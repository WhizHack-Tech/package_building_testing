FROM python:bullseye

COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
#test1

CMD python3 manage.py runserver 0.0.0.0:8000
