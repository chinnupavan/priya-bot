# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
RUN mkdir -p /src/user/app
WORKDIR /src/user/app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python", "main.py"]
