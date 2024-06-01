FROM python:3.11.9-alpine3.19

ADD main.py /app/
ADD core.py /app/
ADD models.py /app/


RUN pip install --upgrade pip

RUN pip install sqlalchemy

RUN pip install psycopg2-binary

RUN pip install alembic

WORKDIR /app/

