# Dockerfile
# Используем Python-образ
FROM python:3.12-slim

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем приложение
COPY . /app
WORKDIR /app

# Указываем порт
ENV PORT 8080

# Запускаем приложение
CMD ["python", "app.py"]
