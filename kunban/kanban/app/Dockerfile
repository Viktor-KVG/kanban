FROM python:3.10.14-alpine3.19

ADD models.py /client/

RUN pip install --upgrade pip

RUN pip install sqlalchemy

RUN pip install psycopg2-binary

WORKDIR /client/