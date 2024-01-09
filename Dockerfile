FROM python:3.10-bullseye

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
#test1

CMD python3 manage.py runserver 0.0.0.0:8000
