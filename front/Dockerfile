FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock .python-version ./

RUN uv sync --frozen --no-install-project
COPY . .
RUN uv sync --frozen
EXPOSE 8050

CMD ["uv", "run", "app/main.py"]