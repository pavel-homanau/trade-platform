FROM python:3.8-slim

WORKDIR /usr/src/app/
COPY Pipfile* /usr/src/app/

RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile

COPY . /usr/src/app/

CMD uvicorn app.main:app --reload --host 0.0.0.0 --port 8000