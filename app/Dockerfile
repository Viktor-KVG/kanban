FROM python:3.11.9-alpine3.19


RUN pip install --upgrade pip

RUN pip install sqlalchemy

RUN pip install psycopg2-binary

RUN pip install alembic

RUN pip install pydantic

RUN pip install fastapi

RUN pip install uvicorn





ADD main.py /app/
ADD core.py /app/
ADD models.py /app/
ADD schemas.py /app/

WORKDIR /app/

