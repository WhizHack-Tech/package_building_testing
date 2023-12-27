FROM ubuntu

ENV PYTHONUNBUFFERED 1

RUN apt update && apt install python3-pip -y && apt autoremove -y && apt clean 
RUN pip3 install wheel pandas cython

COPY dist/ /assets
WORKDIR /assets

RUN python3 compile.py build_ext --inplace && \
    rm controller.py controller.c && \
    rm merger.py merger.c compile.py && \
    mv controller.* controller.so && \
    mv merger.* merger.so && \
    mkdir /app &&  \
    mv *.so *.py *.ini *.sh /app/ && \
    rm -r build
WORKDIR /app

CMD python3 entrypoint.py
