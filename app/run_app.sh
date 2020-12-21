#!/bin/sh

# migrate the database
pipenv run flask db init
pipenv run flask db migrate
pipenv run flask db upgrade

# run the app
exec pipenv run python app.py
# run the app in wsgi
# uwsgi --http 127.0.0.1:5000 --module myproject:app
