FROM debian

ENV DEBIAN_FRONTEND=non-interactive

RUN apt update && \
    apt upgrade -y && \
    apt install git build-essential autoconf automake libtool libxerces-c-dev subversion -y

RUN git clone https://github.com/sk4ld/gridpot.git && \
    cd gridpot/gridlabd/3.1 && \
    autoreconf -isf && \
    make && \
    make install && \
    cd - && \
    cd gridpot/libiec61850-0.8.5 && \
    make && \
    make INSTALL_PREFIX=/usr/local install

WORKDIR /gridpot/gridlabd/3.1/models
CMD gridlabd -D run_realtime=1 --server --debug --verbose IEEE_13_Node_With_Houses.glm