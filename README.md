# Структура проекта

- `src/` - директория с исходными кодами сервиса, основная логика работы
  - `auth/` - директория с аутентификацией через токен
  - `main.py` - точка входа в приложение, где создаётся объект FastAPI и подключаются роутеры.
  - `settings.py` - файл подключения настроек сервиса.
  - `database.py` - файл настройки подключения к БД.
  - `schemas.py` - pydantic схемы для указания формата запросов/ответов api.
  - `models.py` - orm модели таблиц БД (часть слоя Model в нотации MVC, отвечающая за данные).
  - `core.py` - бизнес-логика проекта (часть слоя Model в нотации MVC, отвечающая за поведение).
  - `examples/` - директория для примеров и тестовых скриптов (в реальном проекте такая папка отсутствует!).
- `migrations/` - файлы миграций/ревизий проекта.
- `auth/`
- `alembic.ini` - конфигурация для alembic
- `requirements.txt` - список python-зависимостей проекта.
- `documentation/` - документация проекта.
- `Dockerfile`
- `docker-compose.yml`
- `.gitignore`


# Сборка и запуск проекта

```bash
docker compose build 
docker compose up -d 
```

# Накатывание миграций

Если контейнер с БД развёрнут в первый раз (или после удаления), то необходимо накатить миграции на БД:

```bash
docker exec kanban-main_src_1 alembic upgrade head
```

# Накатывание миграций в тестовой базе данных

```bash
alembic -c alembic_test.ini revision --autogenerate
alembic -c alembic_test.ini upgrade head
```

# swagger

http://127.0.0.1:9000/docs

# Диагностика проблем

Для отображения потоков вывода и потока ошибок внутри контейнера выполнить:

```bash
docker logs -f kanban-main_src_1
```
