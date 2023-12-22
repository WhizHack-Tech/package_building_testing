FROM python:2.7-slim-buster

COPY dist/honeyplc-bin/libsnap7.so-300 /usr/lib/libsnap7.so
COPY dist/honeyplc-bin/server /usr/share/honeyd/s7commServer
WORKDIR /app

# Installing honeyd
RUN apt update && \
    apt upgrade -y && \
    apt install git net-tools lighttpd build-essential libz-dev libevent-dev libdumbnet-dev libpcap-dev libpcre3-dev libedit-dev bison flex libtool automake -y && \
    git clone https://github.com/DataSoft/Honeyd.git && \
    cd Honeyd && \
    mv configure.in configure.ac && \
    ./autogen.sh && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    rm -r Honeyd && \
    chmod 777 /usr/share/honeyd/s7commServer

COPY dist/config.s7-300 /app/config.s7-300
CMD honeyd -d  -f /app/config.s7-300 -u 2000 -g 2000
