FROM python:3.9-slim-buster

LABEL maintainer="rafaella.pinheiro@ufv.br"
LABEL project="AQUA-SENSE - Distributed and IoT Software Architectures"

WORKDIR /app

COPY ./manager /app/manager
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7070

ENV PYTHONPATH="/app"
ENV PYTHONUNBUFFERED=1

CMD ["python3", "manager/api_server.py"]

