FROM python:bullseye

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
#test1
#test2

CMD python3 manage.py runserver 0.0.0.0:8000
