FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /TradePlatform
COPY requirements.txt /TradePlatform/
RUN pip install -r requirements.txt
COPY . /TradePlatform/