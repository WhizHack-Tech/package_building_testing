FROM golang:1.16

ENV GO111MODULE=on
ENV APP_NAME=riotpot
ENV WORKING_DIR=$GOPATH/src/github.com/aau/$APP_NAME

WORKDIR $WORKING_DIR

COPY go.mod .
COPY go.sum .

RUN go mod download
COPY . .
RUN make riotpot-builder && \
    chmod +x build/docker/entrypoint.sh

FROM ubuntu:latest
WORKDIR /root/
RUN apt update && apt install -y netcat && apt upgrade -y && apt autopurge -y && apt clean
COPY --from=0 /go/src/github.com/aau/riotpot ./
CMD ["./build/docker/entrypoint.sh"]