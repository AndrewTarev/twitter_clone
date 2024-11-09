#!/bin/bash

alembic upgrade head

# Команда для запуска приложения
gunicorn backend.src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000