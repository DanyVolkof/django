FROM ubuntu:latest

# Устанавливаем зависимости и необходимые пакеты
RUN apt-get update && \
    apt-get install -y python3 \
    beautifulsoup4 \
    blog \
    certifi \
    charset-normalizer \
    docopt \
    idna \
    jinja2 \
    markdown \
    markupsafe \
    pyembed \
    pyembed-markdown \
    pygments \
    pymdown-extensions \
    pyyaml \
    requests \
    shop \
    soupsieve \
    urllib3


# Копируем файлы вашего сервиса в образ
COPY . /usr/src/app





# Устанавливаем рабочую директорию
WORKDIR /usr/src/app

# Запускаем команды для подготовки сервиса
RUN chmod +x ./startup.sh

# Устанавливаем переменные окружения, если необходимо
ENV django

# Запускаем сервис при запуске контейнера
CMD ["./startup.sh"]