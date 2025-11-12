FROM python:3.13-alpine

RUN apk add --no-cache \
    curl \
    gcc \
    musl-dev \
    mariadb-dev \
    pkgconfig \
    libffi-dev \
    openssl-dev \
    mysql \
    mysql-client

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/scripts/entrypoint.sh

ENTRYPOINT [ "/app/scripts/entrypoint.sh" ]
