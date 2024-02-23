FROM python:3.10
RUN apt update && apt upgrade -y
WORKDIR /app
COPY . .
RUN [ "pip", "install", "-r", "requeriments.txt" ]
ENTRYPOINT [ "make", "docker-entrypoint" ]
