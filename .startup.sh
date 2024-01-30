#!/bin/bash

# Активация виртуального окружения
source /django/Scripts/activate
# Установление зависимостей
pip install -r requirements.txt
# Применение миграции базы данных
python manage.py migrate
# Запуск сервера Django
python manage.py runserver