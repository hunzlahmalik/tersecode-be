#! /bin/bash

if [ "$1" == "format" ]; then
    find . -name '*.py' -not -path "./venv/*" -not -path "**/migrations/*" -exec autopep8 --in-place --aggressive --aggressive '{}' \;
    djlint . --extension=html --reformat
    exit 0
fi

if [ "$1" == "cleanmigrations" ]; then
    find . -path "*/migrations/*.py" -not -path "./venv/*" -not -name "__init__.py" -delete
    find . -path "*/migrations/*.pyc" -not -path "./venv/*" -delete
    exit 0
fi

if [ "$1" == "cleancache" ]; then
    find . -path "*/__pycache__/*" -not -path "./venv/*" -delete
    exit 0
fi

if [ "$1" == "clean" ]; then
    find . -name '*.py' -not -path "./venv/*" -not -path "**/migrations/*" -delete
    find . -path "*/migrations/*.py" -not -path "./venv/*" -not -name "__init__.py" -delete
    find . -path "*/migrations/*.pyc" -not -path "./venv/*" -delete
    find . -path "*/__pycache__/*" -not -path "./venv/*" -delete
    exit 0
fi

if [ "$1" == "celery" ]; then
    celery -A tersecode worker -l info
    exit 0
fi

if [ "$1" == "redis" ]; then
    redis-server
    exit 0
fi

if [ "$1" == "celerybeat" ]; then
    celery -A tersecode beat -l info
    exit 0
fi

if [ "$1" == "run" ]; then
    python manage.py runserver & redis-server & celery -A tersecode worker -l info
    exit 0
fi

if [ "$1" == "--help" ]; then
    echo "Usage: cleanmigrations [--help]"
    echo "Clean migrations files from the project."
    echo "Takes no arguments."

    echo "Usage: format [--help]"
    echo "Format the project codebase."
    echo "Takes no arguments."
    exit 0
fi

