#!/bin/sh

# Wait for the database to be ready
/data_processing_service_docker/wait-for-it.sh db-data-processing-service:5433 --timeout=60 --strict -- echo "[INFO] Database is up for data-processing-service"

# Wait for Redis to be ready
/data_processing_service_docker/wait-for-it.sh data-processing-service-redis:6380 --timeout=60 --strict -- echo "[INFO] Redis is up for data-processing-service"

# Wait for Kafka to be ready
/user_management_service_docker/wait-for-it.sh kafka-user-management-service:9092 --timeout=60 --strict -- echo "[INFO] Kafka is up for data-processing-service"

# Run migrations
echo "[INFO] Running migrations for data-processing-service"
python manage.py makemigrations
python manage.py migrate

# Start the Django development server
echo "[INFO] data-processing-service-docker is up and running"
python manage.py runserver 0.0.0.0:8001
