FROM ghcr.io/astral-sh/uv:0.13.6 AS uv
FROM node:22-bookworm-slim
ARG CODEX_VERSION=0.166.0
ARG CLAUDE_VERSION=2.1.309
COPY --from=uv /uv /usr/local/bin/uv
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev poppler-utils ca-certificates git ripgrep \
    && rm -rf /var/lib/apt/lists/* \
    && npm install -g @openai/codex@${CODEX_VERSION} @anthropic-ai/claude-code@${CLAUDE_VERSION}
COPY agent-env/ /opt/agent-env/
ENV UV_PYTHON_INSTALL_DIR=/opt/python UV_PROJECT_ENVIRONMENT=/opt/agent-venv
RUN uv sync --locked --project /opt/agent-env --python 3.12
RUN useradd --create-home --uid 10001 agent
USER agent
ENV HOME=/home/agent CODEX_HOME=/home/agent/.codex \
    VIRTUAL_ENV=/opt/agent-venv PATH="/opt/agent-venv/bin:${PATH}" \
    ZDOTDIR=/tmp/agent-home BASH_ENV=""
WORKDIR /workspace
