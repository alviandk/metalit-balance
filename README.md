# metalit-balance

### How to make and use virtual environment:

1. Run ```pip install virtualenv```
2. Run ```virtualenv env```
3. For windows, run ```env\Scripts\activate```
4. For linux or macos, run ```source env/bin/activate```

### How to configure project and run django locally
1. Activate virtualenv
2. Run ```cd metalit_balance```
3. Run ```pip install -r requirements.txt```
4. Create and configure .env file
5. Configure local database
6. Run ```python manage.py migrate```
7. Run ```python manage.py runserver``` to run django server locally

### Example of .env file
```
DJANGO_SECRET_KEY = '{DJANGO_SECRET_KEY}'
DJANGO_JWT_KEY = '{DJANGO_JWT_KEY}'
DJANGO_DEV_MODE = '{DJANGO_DEV_MODE}'
DJANGO_DEBUG = '{DJANGO_DEBUG}'
DJANGO_ALLOWED_HOST = '{DJANGO_ALLOWED_HOST}'
DJANGO_DB_NAME = '{DJANGO_DB_NAME}'
DJANGO_DB_USERNAME = '{DJANGO_DB_USERNAME}'
DJANGO_DB_PASSWORD = '{DJANGO_DB_PASSWORD}'
DJANGO_DB_HOST = '{DJANGO_DB_HOST}'
DJANGO_DB_PORT = '{DJANGO_DB_PORT}'
DJANGO_SERVER_TOKEN = '{DJANGO_SERVER_TOKEN}'
```

### How to run test

1. Run virtual environment
2. Run ```cd backend\metalit-challenge```
3. Run ```python manage.py test api.tests.{file_name}```