FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock .python-version ./

RUN uv sync --frozen --no-install-project
COPY . .
RUN uv sync --frozen
EXPOSE 8081

CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8081"]
