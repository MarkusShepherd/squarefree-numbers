"""Provider-independent validation and reproducibility helpers (stdlib only)."""
import copy
import hashlib
import json
import re
from pathlib import Path

# Written by the OS when a folder is browsed: neither corpus content nor agent input.
OS_METADATA = ('.DS_Store',)


def strict_schema(schema):
    """Require every field for both providers; use empty optional values, not omissions."""
    result = copy.deepcopy(schema)
    if 'enum' in result and 'type' not in result:
        result['type'] = 'string'
    if result.get('type') == 'object':
        result['additionalProperties'] = False
        result['properties'] = {k: strict_schema(v) for k, v in result['properties'].items()}
        result['required'] = list(result['properties'])
    elif result.get('type') == 'array':
        result['items'] = strict_schema(result['items'])
    return result


def validate(value, schema, path='$'):
    """Validate the JSON Schema subset used by this repository; fail closed."""
    supported = {'type', 'properties', 'required', 'additionalProperties', 'items', 'enum', 'pattern', 'minItems', 'minimum', 'maximum'}
    if set(schema) - supported:
        raise ValueError(f'{path}: unsupported schema keywords {set(schema) - supported}')
    kind = schema.get('type')
    types = {'object': dict, 'array': list, 'string': str, 'boolean': bool,
             'integer': int, 'number': (int, float)}
    if kind and (not isinstance(value, types[kind]) or kind in ('integer', 'number') and isinstance(value, bool)):
        raise ValueError(f'{path}: expected {kind}')
    if 'enum' in schema and value not in schema['enum']:
        raise ValueError(f'{path}: invalid enum value {value!r}')
    if 'minimum' in schema and value < schema['minimum']:
        raise ValueError(f'{path}: below minimum')
    if 'maximum' in schema and value > schema['maximum']:
        raise ValueError(f'{path}: above maximum')
    if 'pattern' in schema and not re.search(schema['pattern'], value):
        raise ValueError(f'{path}: does not match {schema["pattern"]}')
    if kind == 'object':
        missing = set(schema.get('required', [])) - value.keys()
        extra = value.keys() - schema['properties'].keys()
        if missing or extra and schema.get('additionalProperties') is False:
            raise ValueError(f'{path}: missing {sorted(missing)}, unexpected {sorted(extra)}')
        for key, child in value.items():
            if key in schema['properties']:
                validate(child, schema['properties'][key], f'{path}.{key}')
    if kind == 'array':
        if len(value) < schema.get('minItems', 0):
            raise ValueError(f'{path}: too few items')
        for i, child in enumerate(value):
            validate(child, schema['items'], f'{path}[{i}]')


def digest(path):
    path = Path(path)
    if path.is_symlink():
        # Record the link itself without dereferencing an untrusted agent output.
        return hash_json({"symlink": str(path.readlink())})
    if not path.exists():
        return None
    if path.is_file():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    return hash_json({str(p.relative_to(path)): digest(p) for p in sorted(path.rglob('*'))
                      if (p.is_file() or p.is_symlink()) and p.name not in OS_METADATA})


def hash_json(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def input_hashes(directory):
    if directory.is_symlink():
        return {'.': digest(directory)}
    return {str(p.relative_to(directory)): digest(p) for p in sorted(directory.rglob('*')) if p.is_file() or p.is_symlink()}


def validate_verdict(v):
    if v['verdict'] == 'pass' and v['severity'] not in ('none', 'cosmetic', 'defect-confirmed'):
        raise ValueError('pass verdict cannot have gap/fatal severity')
    if v['verdict'] == 'fail' and v['severity'] not in ('gap', 'fatal'):
        raise ValueError('fail verdict must have gap/fatal severity')
    if (v['verdict'] == 'fail' or v['severity'] == 'defect-confirmed') and not v.get('objection', '').strip():
        raise ValueError('failure/defect requires an actionable objection')


def artifact_files(directory):
    """Numerical deliverables, including nested source modules, without harness metadata."""
    reserved = {'_stream.jsonl', '_stderr.txt', '_last.txt', '_schema.json',
                '_container-version.txt', '_candidate.json'}
    files = {}
    for path in sorted(directory.rglob('*')):
        relative = path.relative_to(directory)
        if path.is_symlink():
            raise ValueError('numerical artifacts must not contain symlinks')
        if any(part in ('.git', '__pycache__') for part in relative.parts):
            continue
        if path.is_file() and relative.parts[0] not in reserved:
            files[str(relative)] = path
    return files


def verify_inputs(directory, expected):
    """A review may add scratch files but must not change any supplied file."""
    actual = input_hashes(directory)
    changed = [name for name, value in expected.items() if actual.get(name) != value]
    if changed:
        raise ValueError('referee modified review inputs: ' + ', '.join(sorted(changed)))


def validate_artifact_tree(directory, missing_ok=False):
    """Reject links and special files before consuming an agent-controlled tree."""
    import stat
    try:
        mode = directory.lstat().st_mode
    except FileNotFoundError:
        if missing_ok:
            return
        raise
    if not stat.S_ISDIR(mode):
        raise ValueError(f'agent outputs contain symlinks or special files: {directory.name}')
    for path in directory.rglob('*'):
        mode = path.lstat().st_mode
        if not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
            raise ValueError(f'agent outputs contain symlinks or special files: {path.relative_to(directory)}')


def read_text_nofollow(path, root):
    """Read a regular response file without following links below a trusted root."""
    import os
    import stat
    parts = path.relative_to(root).parts
    if not parts or any(part in ('.', '..') for part in parts):
        raise ValueError('unsafe final response path')
    directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in parts[:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
            os.close(directory)
            directory = child
        fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
        try:
            if not stat.S_ISREG(os.fstat(fd).st_mode):
                raise ValueError('final response must be a regular file')
            with os.fdopen(fd, encoding='utf-8', closefd=False) as stream:
                return stream.read()
        finally:
            os.close(fd)
    finally:
        os.close(directory)
