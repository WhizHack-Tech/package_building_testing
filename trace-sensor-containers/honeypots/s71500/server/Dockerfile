FROM debian:bullseye

COPY dist/bin /app
WORKDIR /app

RUN apt update && \
    apt upgrade -y && \
    addgroup --gid 2000 honeyplc && \
    adduser --system --no-create-home --shell /bin/bash --uid 2000 --disabled-password --disabled-login --gid 2000 honeyplc && \
    chmod +x /app/s7commServer && \
    mv libsnap7.so-1500 /usr/lib/libsnap7.so && \
    chown honeyplc:honeyplc /usr/lib/libsnap7.so && \
    chown honeyplc:honeyplc /app/s7commServer && \
    mkdir /var/log/honeyplc && \
    chown honeyplc:honeyplc /var/log/honeyplc

USER honeyplc:honeyplc
CMD cd /var/log/honeyplc && /app/s7commServer 0.0.0.0