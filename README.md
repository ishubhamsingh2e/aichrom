# Aichrom Backend Testing Guide

- All the wallpapers are stored in `media/wallpapers`.

## Installation

```shell
cd pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```shell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- api is exposed at localhost:8000/api
- admin is exposed at localhost:8000/admin

## TODO

- [x] Add Endpoint for Wallpapers
- [] Add Endpoint for Icon Packs
