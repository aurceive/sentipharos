# Dockerfile
# Используем Python-образ
FROM python:3.12-slim

# Устанавливаем зависимости
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
COPY server/fes_max/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Копируем кэш модели
COPY server/.cache/st/models--intfloat--e5-mistral-7b-instruct-weightless \
  /root/.cache/st/models--intfloat--e5-mistral-7b-instruct
COPY server/.cache/st/models--intfloat--e5-mistral-7b-instruct/model-00001-of-00003.safetensors \
  /root/.cache/st/models--intfloat--e5-mistral-7b-instruct/model-00001-of-00003.safetensors
COPY server/.cache/st/models--intfloat--e5-mistral-7b-instruct/model-00002-of-00003.safetensors \
  /root/.cache/st/models--intfloat--e5-mistral-7b-instruct/model-00002-of-00003.safetensors
COPY server/.cache/st/models--intfloat--e5-mistral-7b-instruct/model-00003-of-00003.safetensors \
  /root/.cache/st/models--intfloat--e5-mistral-7b-instruct/model-00003-of-00003.safetensors

COPY server/fes_max/app.py app.py

EXPOSE 8080

# Запуск приложения с uvicorn для асинхронного сервера
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]

# fes — feature extraction service

# docker build -t gcr.io/sentipharos/fes-max --file server/fes_max/Dockerfile .
# docker push gcr.io/sentipharos/fes-max

# gcloud run deploy fes-max --image gcr.io/sentipharos/fes-max --platform managed --timeout 5m --region europe-north1
#   --allow-unauthenticated --memory 32Gi --cpu 8 --max-instances 1

# gcloud run services update fes-max --region europe-north1 --memory 14Gi --cpu 8
# gcloud run services update fes-max --region europe-north1 --concurrency 80