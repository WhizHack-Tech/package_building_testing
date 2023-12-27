FROM alpine:3.16

RUN apk -U --no-cache add \
              git \
	      libcap \
              py3-libxml2 \
              py3-lxml \
	      py3-pip \
              python3 \
              python3-dev \
              tshark && \
    addgroup -g 2000 fatt && \
    adduser -S -s /bin/ash -u 2000 -D -g 2000 fatt && \
    mkdir -p /opt && \
    cd /opt && \
    git clone https://github.com/0x4D31/fatt && \
    cd fatt && \
    git checkout c29e553514281e50781f86932b82337a5ada5640 && \
    mkdir -p log && \
    pip3 install pyshark==0.4.2.11 && \
    chgrp fatt /usr/bin/dumpcap && \
    setcap cap_net_raw,cap_net_admin=+eip /usr/bin/dumpcap && \
    chown fatt:fatt -R /opt/fatt/* && \
    mkdir -p /var/log/zerohack/fatt && \
    chown -R fatt:fatt /var/log/zerohack/fatt && \
    apk del --purge git \
                    python3-dev && \
    rm -rf /root/* /var/cache/apk/* /opt/fatt/.git

STOPSIGNAL SIGINT
ENV PYTHONPATH /opt/fatt
WORKDIR /opt/fatt
CMD python3 fatt.py -i $(if [ -z "$MONITOR_INT" ]; then echo $(/sbin/ip address show | /usr/bin/awk '/inet.*brd/{ print $NF; exit }'); else echo $MONITOR_INT; fi) --print_output --json_logging -o /var/log/zerohack/fatt/fatt.log
