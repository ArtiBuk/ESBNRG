# Указываем базовый образ, содержащий Python
FROM python:3.10

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости проекта (файлы requirements.txt)
COPY ./requirements.txt /app/

# Устанавливаем зависимости проекта
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все содержимое директории "ESB" в рабочую директорию контейнера
COPY ESB/ /app/

# Запускаем команду для миграции базы данных (при необходимости)
# RUN python manage.py migrate

# Указываем порт, который будет использоваться в контейнере
EXPOSE 8000

# Команда для запуска Django приложения при старте контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
