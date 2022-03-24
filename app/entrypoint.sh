#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

if [ "$MIGRATIONS" = "true" ]
then
    python manage.py flush --no-input
    python manage.py migrate
    python manage.py shell -c """
from django.contrib.auth import get_user_model;
get_user_model().objects.create_superuser(email='admin@gmail.com', password='password')
    """
fi

exec "$@"