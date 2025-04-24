# Используем официальный образ Python
FROM python:3.11-slim-bullseye

# Устанавливаем переменные среды
ENV PYTHONDONTWRITEBYTECODE 1  # Не создавать .pyc файлы
ENV PYTHONUNBUFFERED 1         # Не буферизовать stdout/stderr

# Устанавливаем системные зависимости для psycopg2
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#     libpq-dev \
#     gcc \
#     python3-dev && \
#     rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем необходимые пакеты для сборки (например, для psycopg2)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY . .

# Собираем статику , это упрощает развертывание, т.к. статика уже в образе
RUN python manage.py collectstatic --noinput

# Меняем пользователя на непривилегированного (если нужно, создайте этого пользователя)
# RUN useradd -m myuser && chown -R myuser /app
# USER myuser

# Указываем порт, который будет прослушивать контейнер
EXPOSE 10000

# Команда для запуска сервера
CMD ["gunicorn", "get_ready.wsgi:application", "--bind", "0.0.0.0:10000"]

# (для development)
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]