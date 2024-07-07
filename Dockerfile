# Используем базоый образ на основе дистрибутива bookworm (debian 12)
FROM python:3.9.19-bookworm

# Обновляем системные пакеты
RUN apt update \
    && apt -y upgrade\
    && apt install -y htop
# Обновляем pip до фиксированной версии
RUN pip install pip==24.0
# Создаём технического пользователя, от имени которого будет работать сервис (не root)
RUN useradd -s /bin/bash -m kanban

# Создаём директорию для проекта и меняем владельца с root на технического пользователя
RUN mkdir -p /app
# Назначаем директорию проекта рабочей директорией
WORKDIR /app/

# Копируем в директорию для проекта файл с указанием зависимостей для python
COPY ./requirements.txt /app/requirements.txt
# Устанавливаем все python зависимости
RUN pip install -r requirements.txt
# Удаляем файл с указанием зависимостей
RUN rm /app/requirements.txt

# Меняем владельца с root на технического пользователя
RUN chown -R kanban:kanban /app
# Переключаемся в технического пользователя
USER kanban

# Устанавливаем дефолтную точку входа
# ENTRYPOINT "bash"
# ENTRYPOINT [ "bash"]
# CMD "bash"
CMD [ "bash" ]
