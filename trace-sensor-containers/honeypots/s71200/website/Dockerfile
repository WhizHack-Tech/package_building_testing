FROM httpd:2.4.54-bullseye

COPY dist/website /usr/local/apache2/htdocs

RUN apt update && \
    apt upgrade -y && \
    cd /usr/local/apache2/htdocs && \
    tar -xvf website.tar