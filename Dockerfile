FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


# inside Dockerfile
CMD ["celery", "-A", "app.celery_worker.celery", "worker", "--loglevel=info"]
