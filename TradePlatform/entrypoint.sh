#!/bin/bash
set -ex
#flake8
#mypy TradePlatform/
#pylint TradePlatform/
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000