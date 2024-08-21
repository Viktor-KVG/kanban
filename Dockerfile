FROM python:3.11.9-alpine3.19


RUN pip install --upgrade pip

# Копируем файл requirements.txt в контейнер
COPY requirements.txt /kanban-main/requirements.txt

# Устанавливаем зависимости
RUN pip install -r /kanban-main/requirements.txt

# Копируем весь код в контейнер
COPY . /kanban-main

# Устанавливаем рабочую директорию
WORKDIR /kanban-main


CMD [ "uvicorn src.main:app --reload" ]

