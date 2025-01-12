FROM python:3.12-slim

COPY server/worker/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY /server/worker /server/worker
COPY /server/db /server/db

WORKDIR /
CMD ["python", "-m", "server.worker.app"]

# docker build -t gcr.io/sentipharos/worker -f server/worker/Dockerfile .
# docker push gcr.io/sentipharos/worker

# gcloud compute instances create-with-container worker --project=sentipharos --zone=us-central1-c --machine-type=e2-micro
#   --maintenance-policy=MIGRATE --provisioning-model=STANDARD --boot-disk-size=10GB --boot-disk-device-name=worker
#   --boot-disk-type=pd-standard --container-image=gcr.io/sentipharos/worker


# gcloud compute instances update-container worker --container-image=gcr.io/sentipharos/worker --zone=us-central1-c
