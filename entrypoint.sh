# add this file because the api service is dependent on:
# a) container up and running 
# b) Postgres instance healthy and up

#!/bin/sh

echo "Waiting for postgres..."

# reference Postgres container using api-db as the name of the service. Loop continues until it returns
# Connection to api-db port 5432 [tcp/postgresql] succeded.
while ! nc -z api-db 5432; do
    sleep 0.1
done

echo "PostgreSQL started"

python manage.py run -h 0.0.0.0