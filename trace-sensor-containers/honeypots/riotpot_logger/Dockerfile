FROM ubuntu:latest

RUN apt update && \
    apt upgrade -y && \
    apt install -y python3-pip && \
    pip3 install pandas SQLAlchemy psycopg2-binary && \
    mkdir /var/log/riotpot /app && \
    addgroup --gid 2000 zhtrap && \
    adduser --system --no-create-home --uid 2000 --disabled-password --disabled-login --gid 2000 zhtrap && \
    chmod 770 -R /var/log/riotpot && \
    chown -R zhtrap:zhtrap /var/log/riotpot /app && \
    apt autopurge -y && \
    rm -rf /var/lib/apt/lists/*

COPY /dist /app
ENV PYTHONUNBUFFERED 1
USER zhtrap:zhtrap
WORKDIR /app
CMD python3 logger.py