FROM alpine:3.16
#
# Setup apk
RUN apk -U --no-cache add \
                   build-base \
                   git \
                   go \
                   g++ && \
# Setup go, build medpot
    export GOPATH=/tmp && \
    cd /tmp && \
    git clone https://github.com/s9rA16Bf4/medpot.git && \
    cd medpot && \
    go mod tidy && \
    git checkout 0feb786cd8a7616498ba9749dbfda24b5dbd363e && \
    sed -i s/"ews = true"/"ews = false"/g template/ews.cfg && \
    go build -o medpot go/medpot.go go/logo.go && \
    mkdir -p /etc/medpot \
             /opt/medpot \
             /var/log/medpot && \
    cp medpot /opt/medpot && \
    cp ./template/* /etc/medpot && \
#
# Setup user, groups and configs
    addgroup -g 2000 medpot && \
    adduser -S -s /bin/ash -u 2000 -D -g 2000 medpot && \
    chown -R medpot:medpot /var/log/medpot && \
#
# Clean up
    apk del --purge build-base \
                    git \
                    go \
                    g++ && \
    rm -rf /var/cache/apk/* \
           /opt/go \
           /root/dist \
	   /tmp
#
# Start medpot
WORKDIR /opt/medpot
USER medpot:medpot
CMD ["./medpot"]