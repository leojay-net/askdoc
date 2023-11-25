#!/bin/bash
python -m pip install --upgrade pip

pip install -r requirements.txt

pip install --upgrade openai

python manage.py makemigrations

python manage.py collectstatic --no-input

python manage.py migrate

python manage.py spectacular --file schema.yml