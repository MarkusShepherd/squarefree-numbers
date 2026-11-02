#!/usr/bin/env python3
"""One ephemeral container per invocation; only the agent folder and login are mounted."""
import argparse
import os
from pathlib import Path
import signal
import subprocess
import sys
import uuid


def command(image, workdir, outputs, backend, cli, environ, readonly=False):
    name = 'sqf-' + uuid.uuid4().hex
    cmd = ['docker', 'run', '--rm', '--name', name, '--init', '--cap-drop=ALL',
           '--security-opt=no-new-privileges', '--pids-limit=256', '--read-only',
           '--user', f'{os.getuid()}:{os.getgid()}',
           '--tmpfs', '/tmp:rw,nosuid,nodev,mode=1777',
           '--env', 'HOME=/tmp/agent-home', '--env', 'CODEX_HOME=/tmp/agent-home/.codex',
           '--env', 'CLAUDE_CONFIG_DIR=/tmp/agent-home/.claude',
           '--mount', f'type=bind,src={workdir},dst=/workspace' + (',readonly' if readonly else ''),
           '--mount', f'type=bind,src={outputs},dst=/outputs', '--workdir', '/workspace']
    if backend == 'codex':
        auth = Path(environ.get('CODEX_AUTH_FILE', str(Path.home() / '.codex/auth.json'))).expanduser()
        if not auth.is_file():
            raise ValueError('Codex container requires CODEX_AUTH_FILE (defaults to ~/.codex/auth.json)')
        # Copy just the login into the ephemeral container's own home; refreshes stay local.
        cmd += ['--mount', f'type=bind,src={auth.resolve()},dst=/tmp/codex-auth.json,readonly']
        setup = 'set -eu; mkdir -p "$CODEX_HOME"; cp /tmp/codex-auth.json "$CODEX_HOME/auth.json"; '
    else:
        if not environ.get('CLAUDE_CODE_OAUTH_TOKEN'):
            raise ValueError('Claude container requires CLAUDE_CODE_OAUTH_TOKEN from claude setup-token')
        cmd += ['--env', 'CLAUDE_CODE_OAUTH_TOKEN', '--env', 'ENABLE_CLAUDEAI_MCP_SERVERS=false',
                '--env', 'CLAUDE_CODE_EFFORT_LEVEL']
        setup = 'set -eu; mkdir -p "$HOME"; '
    # Never evaluate the model's prompt as shell source. Positional argv preserves it verbatim.
    setup += '"$1" --version > /outputs/_container-version.txt; exec "$@"'
    return name, cmd + [image, 'sh', '-c', setup, 'sqf-agent', *cli]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', required=True)
    parser.add_argument('--workdir', required=True)
    parser.add_argument('--outputs', required=True)
    parser.add_argument('--readonly-workspace', action='store_true')
    parser.add_argument('--backend', choices=['claude', 'codex'], required=True)
    parser.add_argument('cli', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    cli = args.cli[1:] if args.cli[:1] == ['--'] else args.cli
    if not cli:
        parser.error('missing provider invocation')
    # The provider is installed in the image; host paths must never be mounted to find it.
    cli[0] = args.backend
    outputs = Path(args.outputs).resolve()
    outputs.mkdir(parents=True, exist_ok=True)
    try:
        name, cmd = command(args.image, str(Path(args.workdir).resolve()), str(outputs), args.backend, cli, os.environ, args.readonly_workspace)
    except ValueError as e:
        parser.exit(1, str(e) + '\n')

    def stop(signum, frame):
        raise SystemExit(128 + signum)

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    try:
        return subprocess.call(cmd)
    finally:
        # Killing the Docker client alone does not stop its container.
        subprocess.run(['docker', 'rm', '--force', name], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, timeout=4)


if __name__ == '__main__':
    sys.exit(main())
