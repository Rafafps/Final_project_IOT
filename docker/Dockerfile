FROM python:3.9-slim-buster

LABEL maintainer="rafaella.pinheiro@ufv.br"
LABEL project="AQUA-SENSE - Distributed and IoT Software Architectures"

WORKDIR /app

COPY ./manager /app/manager
COPY ./config /app/config
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7070

ENV PYTHONPATH="/app"
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "manager.api_server:app", "--host", "0.0.0.0", "--port", "7070"]

