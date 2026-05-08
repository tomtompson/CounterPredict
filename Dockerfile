FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim

# Set working directory
WORKDIR /app

# Set uv environment variables for better Docker performance
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1

COPY pyproject.toml uv.lock ./
COPY app/ ./app/

RUN uv pip install --system -r pyproject.toml

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${API_PORT}"]
