#!/bin/sh

# migrate the database
pipenv run flask db init
pipenv run flask db migrate
pipenv run flask db upgrade

# run the app
# exec pipenv run python app.py
# run app in wsgi/gunicorn in production
# uwsgi --http 127.0.0.1:8000 --module myproject:app
gunicorn --workers=1 --bind=0.0.0.0:8000 app:app
