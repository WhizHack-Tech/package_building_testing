FROM python:3.9-slim-bullseye

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/requirements.txt
WORKDIR /app

# Setting up the OS.
RUN apt update && apt upgrade -y && apt autoremove -y && apt clean && apt install libgomp1 -y 

# Installing dependencies
RUN pip3 install -r requirements.txt

#test1
#test4
#test5
#test6

COPY dist/ /app
CMD python3 global_feed.py && python3 controller.py
