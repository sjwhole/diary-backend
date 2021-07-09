# Diary

REST API for my diary app

# Installation

Clone the source code and use [Docker](https://www.docker.com/) for build:

```bash
docker-compose up --build -d
```

Migrate models to database:

```bash
docker-compose exec api python manage.py makemigrations 
docker-compose exec api python manage.py migrate 
```

To fix the static files unloaded:

```bash
docker-compose exec api python manage.py collectstatic --noinput
```