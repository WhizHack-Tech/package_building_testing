FROM golang:bullseye AS builder

COPY dist/ /app/
WORKDIR /app

RUN apt update && apt install libpcap-dev -y && \
    go mod download && \
    go build

FROM ubuntu:20.04

RUN apt update && \
    apt upgrade -y && \
    apt install tcpdump iproute2 ca-certificates curl -y && \
    apt autoremove -y && \
    apt clean && \
    mkdir -p /var/log/zerohack/photon/storage/artifacts/http && \
    mkdir -p /var/log/zerohack/photon/storage/rules

COPY --from=builder /app/photon /app/photon
WORKDIR /app
CMD ./photon -i $(if [ -z "$MONITOR_INT" ]; then echo $(/sbin/ip address show | /usr/bin/awk '/inet.*brd/{ print $NF; exit }'); else echo $MONITOR_INT; fi) -operation_environment $SENSOR_NAME