FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app/
COPY Pipfile* /usr/src/app/

RUN pip install pipenv && pipenv install --deploy --system --ignore-pipfile

COPY entrypoint.sh /usr/src/app/
RUN chmod +x entrypoint.sh

COPY . /usr/src/app/

ENTRYPOINT ["sh", "./entrypoint.sh"]