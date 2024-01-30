FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /shops_online

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.0 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"


COPY pyproject.toml poetry.lock /shops_online/
RUN pip install poetry
RUN poetry install --no-dev
   
# Копируем файлы вашего сервиса в образ
COPY . /shops_online

# Запускаем команды для подготовки сервиса
RUN chmod +x .startup.sh

# Запускаем сервис при запуске контейнера
CMD [".startup.sh"]