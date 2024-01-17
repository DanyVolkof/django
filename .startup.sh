#!/bin/bash
# Переход в директорию с проектом
cd /D:/shops_online/shop
# Активация виртуального окружения
source /django/Scripts/activate
# Установление зависимостей
pip install -r poetry.lock
# Применение миграции базы данных
python manage.py migrate
# Запуск сервера Django
python manage.py runserver