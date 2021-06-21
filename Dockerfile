# pull official base image. Pull slim-buster-based Docker image for Python 3.9.5
FROM python:3.9.5-slim-buster

#set working directory
WORKDIR /usr/src/app

#set environment variables
#PYTHONDONTWRITEBYTECODE prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
#PYTHONUNBUFFERED prevents Python from buffering stdout and stderr 
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
 && apt-get -y install netcat gcc postgresql \
 && apt-get clean

#add and install requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt

#add app
COPY . .

# TODO: add entrypoint.sh
# COPY ./entrypoint.sh .
# RUN chmod 777 /usr/src/app/entrypoint.sh

#run server
CMD python manage.py run -h 0.0.0.0