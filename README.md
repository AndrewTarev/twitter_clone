# Twitter_clone | FastAPI

API для корпоративного сервиса микроблогов, который умеет отправлять твиты, удалять, лайкать посты и т.д

## Contents

- [App Structure](#app-structure)
- [Technologies](#technologies)
- [How to use API](#how-to-use-api)
- [How to launch application](#how-to-launch-application)
- [How to run test environment](#how-to-run-test-environment)
- [Example](#example)

## App Structure

- [fastapi-app](#fastapi-app)
  - [Database](#database)
  - [Routers](#routers)
  - [Other](#other)

## Technologies

- **FastAPI** - Для быстрых запросов с использованием асинхронности
- **PostgreSQL** - Для удобного хранения данных. Имеет множество типов данных, что позволяет использовать такой тип данных как ARRAY и др
- **Nginx** - Для быстрой раздачи статики, а также многопользовательской поддержки сайта
- **Alembic** - Для удобного создания таблиц в бд при запуске приложения
- **SQLAlchemy ORM** - Для создания моделей (Python Class) и запросов к бд

## fastapi-app

### Database

#### business_logic

- **followers** - логика по работе с фолловерами
- **likes** - логика по работе с лайками
- **medias** - логика по работе с загрузкой медиа
- **tweets** - логика по работе с твитами
- **users** - логика по работе с пользователями

#### Other files

- **config** - Конфигурационные настройки, например определение URL
- **connection** - найстройки самого подключения, определение session, engine
- **models** - ORM модели
- **schemas** - схемы pydantic для валидации данных

### Routers

- **medias** - эндпоинты по работе с загрузкой изображений
- **tweets** - эндпоинты по работы с твитами (создание, удаление, т.д)
- **users** - эндпоинты по работе со пользвоателями (получение информации, т.д)

### Other

- **application** - Основной файл для запуска приложения
- **dependencies** - зависимости Fastapi для эндпоинтов
- **migrations** - папка с системными файлами alembic, а также сами файлы миграций
- **alembic.ini** - конфигурационный файл, необходимый при запуске миграций
- **static** - папка с статическими файлы, такими как css, js, images и т.д

## How to use API

У FastAPI есть документирование Swagger, поэтому вы можете посмотреть как использовать API по след ссылке

- `/docs`

## How to launch application

- Создать .env файл на основе шаблона .env.template


- `docker compose up --build` - Запуск контейнеров Postgres, Api - приложения

## How to run test environment

- `docker compose -f docker-compose-test.yml up -d` - Запуск контейнеров Postgres, Тестового окружения


## Example
