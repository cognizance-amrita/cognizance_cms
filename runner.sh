#! /bin/bash
virtualenv python3
source python3/bin/activate
pip3 install -r requirements.txt
python3 manage.py createsuperuser
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver

echo "Interrupted."
