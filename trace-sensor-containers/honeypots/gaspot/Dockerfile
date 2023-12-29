FROM alpine 

WORKDIR /app
COPY dist /app

RUN apk update && \
    apk add python3 && \
    addgroup -g 2000 gaspot && \
    adduser -S -s /bin/ash -u 2000 -D -g 2000 gaspot && \
    mkdir -p /var/log/gaspot && \
    chown -R gaspot:gaspot /var/log/gaspot

USER gaspot:gaspot
CMD python3 GasPot.py --log /var/log/gaspot/gaspot.log