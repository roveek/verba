# Базовый Python-образ
FROM python:3.13-slim

# Кладём uv и uvx в /bin (официальный один бинарь)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Опционально: системные зависимости (для playwright-браузеров)
RUN apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    libnss3 \
    libx11-6 \
    libxkbcommon0 \
    libxcomposite1 \
    libxrandr2 \
    libxi6 \
    libgtk-3-0 \
    libglib2.0-0 \
    libdrm2 \
    libgbm1 \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы проекта
COPY pyproject.toml ./
COPY src/* ./

# Устанавливаем зависимости через uv
RUN uv sync --no-cache --no-editable

# Ставим браузеры Playwright
RUN uv run playwright install

# Запуск скрипта
CMD ["uv", "run", "python", "main.py"]
