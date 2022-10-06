#!/bin/sh

if [ "$POSTGRES_DB" = "postgres" ]
cmd="$@"
timer="5"
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep timer
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input

exec "$@"