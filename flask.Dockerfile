# Partim de la imatge oficial: https://hub.docker.com/_/python
FROM python:3.9.18-bookworm

# Definim el directori de treball
WORKDIR /usr/src/app

# Definim les variables d'entorn
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instal·lem les dependències
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt