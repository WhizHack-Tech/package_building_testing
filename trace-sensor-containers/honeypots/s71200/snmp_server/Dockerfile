FROM python:3

COPY dist /app
RUN pip3 install snmpsim && \
    addgroup --gid 2000 snmpsim && \
    adduser --system --no-create-home --uid 2000 --disabled-password --disabled-login --gid 2000 snmpsim

USER snmpsim:snmpsim
CMD snmpsimd.py --data-dir=/app --agent-udpv4-endpoint=0.0.0.0:1024