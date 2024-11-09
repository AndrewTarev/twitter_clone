FROM python:3.12-slim

RUN mkdir /app

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --only main

COPY . .

CMD ["uvicorn", "backend.src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]


