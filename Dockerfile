FROM python:3.9-slim-buster

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock README.md ./
COPY src/ ./src/

RUN poetry install --no-interaction --no-ansi