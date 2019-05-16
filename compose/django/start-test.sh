#!/bin/sh

python manage.py migrate

if [ "$PYTEST_WATCH" = "1" ]
then
    ptw
else
    pytest
fi
