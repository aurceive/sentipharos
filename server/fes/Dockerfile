# Dockerfile
# Используем Python-образ
FROM python:3.12-slim

# Устанавливаем зависимости
COPY server/fes/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Копируем кэш модели
COPY server/.cache/st/models--intfloat--multilingual-e5-large-instruct \
  /root/.cache/st/models--intfloat--multilingual-e5-large-instruct

COPY server/fes/app.py app.py

WORKDIR /

EXPOSE 8080

# Запуск приложения с uvicorn для асинхронного сервера
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]

# fes — feature extraction service

# docker build -t gcr.io/sentipharos/fes --file server/fes/Dockerfile .
# docker push gcr.io/sentipharos/fes

# gcloud run deploy fes --image gcr.io/sentipharos/fes --platform managed --timeout 5m
#   --region europe-north1 --allow-unauthenticated --memory 5Gi --cpu 2 --max-instances 1

# gcloud run services update fes --region europe-north1 --memory 8Gi --cpu 4
# gcloud run services update fes --region europe-north1 --concurrency 80
# gcloud run services update fes --region europe-north1 --timeout 10m