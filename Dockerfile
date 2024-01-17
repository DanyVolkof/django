FROM python:3.10-slim
# Устанавливаем зависимости и необходимые пакеты
RUN apt-get update && \
    apt-get install -y python3 \
    asgiref \
    certifi \
    channels \
    charset-normalizer \
    datetime \
    django \
    django-channels \
    django4-background-tasks \
    djangorestframework \
    djangorestframework-simplejwt \
    drf-yasg \
    idna \
    inflection \
    numpy \
    oauthlib \
    packaging \
    pandas \
    pyjwt \
    python-dateutil \
    pytz \
    pyyaml \
    requests \
    requests-oauthlib \
    setuptools \
    six \
    sqlparse \
    timedelta \
    tzdata \
    uritemplate \
    urllib3 \
    whitenoise \
    zope-interface \
# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы вашего сервиса в образ
COPY . .

# Запускаем команды для подготовки сервиса
RUN chmod +x ./startup.sh

# Устанавливаем переменные окружения, если необходимо
ENV django

# Запускаем сервис при запуске контейнера
CMD ["./startup.sh"]