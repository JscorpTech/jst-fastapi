#!/bin/sh

# wait for postgres to start
while ! nc -z db 5432 ; do
    echo "Waiting for postgres..."
    sleep 1
done

# Apply database migrations
echo "Apply database migrations"
alembic upgrade head

# Start FastAPI
echo "Starting FastAPI"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
