#! bash

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

if [ "$1" == "--help" ]; then
    echo "Usage: cleanmigrations [--help]"
    echo "Clean migrations files from the project."
    echo "Takes no arguments."

    echo "Usage: format [--help]"
    echo "Format the project codebase."
    echo "Takes no arguments."
    exit 0
fi