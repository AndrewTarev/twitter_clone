#!/bin/bash

alembic upgrade head

# Команда для запуска приложения
uvicorn backend.src.main:app --reload --host 0.0.0.0 --port 8000