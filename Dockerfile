FROM python:3.10
RUN apt update && apt upgrade -y
WORKDIR /app
COPY . .
RUN pip install poetry
RUN [ "make", "setup" ]
ENTRYPOINT [ "make", "create-report" ]
