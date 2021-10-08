FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY Pipfile* /app/

RUN pip install pipenv && pipenv install --deploy --system --ignore-pipfile

COPY entrypoint.sh /app/
RUN chmod +x entrypoint.sh

COPY . /app/

ENTRYPOINT ["sh", "./entrypoint.sh"]