FROM fluentd:v1.16.0-debian-1.0

USER root

RUN apt update && \
    apt upgrade -y && \
    apt install ruby-dev build-essential libgeoip-dev libmaxminddb-dev curl bzip2 aria2 autoconf libtool -y && \
    mkdir -p /etc/listbot && \
    gem install geoip2_c && \
    fluent-gem install fluent-plugin-s3 --no-document && \
    fluent-gem install fluent-plugin-opensearch --no-document && \
    fluent-gem install fluent-plugin-record-modifier --no-document && \
    fluent-gem install fluent-plugin-grok-parser --no-document && \
    fluent-gem install fluent-plugin-geoip --no-document && \
    fluent-gem install fluent-plugin-dict-map --no-document && \
    fluent-gem install fluent-plugin-dedot_filter --no-document && \
    apt autopurge build-essential ruby-dev -y && \
    gem sources --clear-all  && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/* /var/tmp/* /usr/lib/ruby/gems/*/cache/*.gem && \
    chown -R fluent:fluent /etc/listbot && \
    echo "[*] Updating IP translation maps." && \
    aria2c -s16 -x 16 https://get.zerohack.in/reputations/cve.json.bz2 && \
    aria2c -s16 -x 16 https://get.zerohack.in/reputations/iprep.json.bz2 && \
    bunzip2 -f *.bz2 && \
    cp cve.json /etc/listbot && \
    cp iprep.json /etc/listbot

COPY dist/geo-data /geo-data
COPY dist/cacert.pem /etc/cacert.pem
RUN cp /etc/cacert.pem /usr/local/share/ca-certificates/ && update-ca-certificates
COPY dist/entrypoint.sh /bin/
COPY dist/fluent.conf /fluentd/etc/
