#!/bin/bash

while !</dev/tcp/db/5432; do echo "waiting for db..." && sleep 1; done;
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
