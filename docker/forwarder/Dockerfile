# Heres a puzzle for the brave ones.
# There is 200 MBs worth of junk here. Lets see if you are smart enough to find it.
FROM fluentd:v1.14.0-debian-1.0

USER root

RUN apt update && \
    apt upgrade -y && \
    apt install ruby-dev build-essential libgeoip-dev libmaxminddb-dev curl bzip2 aria2 -y && \
    mkdir -p /etc/listbot && \
    fluent-gem install fluent-plugin-s3 --no-document && \
    fluent-gem install fluent-plugin-dedot_filter --no-document && \
    fluent-gem install fluent-plugin-record-modifier --no-document && \
    apt autopurge build-essential ruby-dev -y && \
    gem sources --clear-all  && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/* /var/tmp/* /usr/lib/ruby/gems/*/cache/*.gem && \
    chown -R fluent:fluent /etc/listbot

COPY dist/geo-data /geo-data
#COPY dist/cacert.pem /etc/cacert.pem
COPY dist/entrypoint.sh /bin/
COPY dist/fluent.conf /fluentd/etc/
