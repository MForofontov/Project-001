# Environment Variables for `.env`

Below is a list of all the environment variables required for the project. Replace placeholder values (`your_*`) with actual values specific to your environment.

---

## **User Management Service**
POSTGRES_USER_UMS=your_user
POSTGRES_PASSWORD_UMS=your_password
POSTGRES_DB_UMS=your_db
DB_PORT_UMS=5432
DB_HOST_UMS=your_host

DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,admin.localhost,user-management-service

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=your_google_redirect_uri

EMAIL_HOST=your_email_host
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email_user
EMAIL_HOST_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=your_default_email
EMAIL_VERIFICATION_SALT=email-verification-salt

USER_MANAGEMENT_SERVICE_REDIS_HOST=redis-user-management-service
USER_MANAGEMENT_SERVICE_REDIS_PORT=6379
USER_MANAGEMENT_SERVICE_REDIS_DB=0
USER_MANAGEMENT_SERVICE_REDIS_PASSWORD=your_redis_password
USER_MANAGEMENT_SERVICE_REDIS_URL=redis://redis-user-management-service:6379/0

USER_MANAGEMENT_SERVICE_CELERY_BROKER_URL=redis://redis-user-management-service:6379/0
USER_MANAGEMENT_SERVICE_CELERY_RESULT_BACKEND=redis://redis-user-management-service:6379/0

FRONTEND_URL=http://localhost:5173

## **Data Processing Service**
POSTGRES_USER_DPS=your_user
POSTGRES_PASSWORD_DPS=your_password
POSTGRES_DB_DPS=your_db
DB_PORT_DPS=5433
DB_HOST_DPS=your_host

DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,admin.localhost

CORS_ALLOWED_ORIGINS=http://localhost:5173
CSRF_TRUSTED_ORIGINS=http://localhost:5173

CELERY_BROKER_URL=redis://data-processing-service-redis:6379/0
CELERY_RESULT_BACKEND=redis://data-processing-service-redis:6379/0

## **Frontend**
REACT_APP_GOOGLE_ANALYTICS_ID=your_google_analytics_id

## **Prometheus**
PROMETHEUS_SCRAPE_INTERVAL=15s

## **Kafka**
KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1
KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1
KAFKA_TRANSACTION_STATE_LOG_MIN_ISR=1
KAFKA_MIN_INSYNC_REPLICAS=1
KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS=0