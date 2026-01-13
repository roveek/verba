# Базовый Python-образ
FROM python:3.13-slim

# Кладём uv и uvx в /bin (официальный один бинарь)
# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml ./
COPY src/* ./

RUN uv sync

RUN uv run playwright install

CMD ["uv", "run", "python", "main.py"]
