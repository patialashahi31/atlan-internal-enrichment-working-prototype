# Dockerfile
FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
RUN apt update && apt install -y curl vim

CMD ["python", "app.py"]
