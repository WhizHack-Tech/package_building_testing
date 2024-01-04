FROM alpine:3.14

# Include dist
ADD dist/ /root/dist/

# Install packages
RUN apk update && \
    apk upgrade && \
    apk -U --no-cache add ca-certificates curl file hiredis libcap wget suricata && \
    # Setup user, groups and configs
    addgroup -g 2000 suri && \
    adduser -S -H -u 2000 -D -g 2000 suri && \
    chmod 644 /etc/suricata/*.config && \
    cp /root/dist/*.yaml /etc/suricata/ && \
    cp /root/dist/*.conf /etc/suricata/ && \
    cp /root/dist/*.bpf /etc/suricata/ && \
    # Download the latest EmergingThreats OPEN ruleset
    tar -xvf /root/dist/etpro.rules.tar.gz && \
    rm -rf /root/dist/etpro.rules.tar.gz && \
    cp rules/* /var/lib/suricata/rules/ && \
    #cp /root/dist/update.sh /usr/bin/ && \
    #chmod 755 /usr/bin/update.sh && \
    #suricata-update update-sources && \
    #suricata-update --no-reload && \
    # Clean up
    rm -rf /root/* && \
    rm -rf /tmp/* && \
    rm -rf /var/cache/apk/*

#test test1
#test test2 
#test test3 
#test test4 
#test test5
#test6
#test7
#test8
#test9
#test10
#test11
#test12
#test13
#test14
#test15
#test16
#test17
#test18
#test19

# Start suricata
STOPSIGNAL SIGINT
CMD suricata -v -i $(/sbin/ip address show | /usr/bin/awk '/inet.*brd/{ print $NF; exit }')
