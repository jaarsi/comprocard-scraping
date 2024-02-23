FROM python:3.10
RUN apt update && apt upgrade -y
WORKDIR /app
COPY . .
RUN [ "pip", "install", "-r", "requirements.txt" ]
ENTRYPOINT [ "./scripts/create-report.sh" ]
