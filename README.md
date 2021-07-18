# Discourse

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/triplinker/triplinker/blob/master/LICENSE)

---

## Getting Started

These instructions will help you to get the copy of the project for development and testing purposes.

## Running Locally

### Clone the project to your local machine

```
git clone https://github.com/GonnaFlyMethod/discourse-django-vue
```

### Install poetry  

```
pip install poetry
```

### Install all dependencies

***Note:*** before that you need to get to the directory with the project, then you can write the command below: 

```
poetry install
```

### Create .env file near the manage.py file 

***Note:*** .env will be invisible, so make it visible and set the following values inside: 

```
DEBUG=on
SECRET_KEY="dev"
DATABASE_URL=psql://test:test@127.0.0.1:5432/test
STATIC_URL=/static/
```

If you are using another DB for development then check the [documentation](https://django-environ.readthedocs.io/en/latest/) out for more information. 
### Create database

```
sudo -u postgres psql
```

Enter the password and then write:

```
CREATE DATABASE test;
```

### Create user in the DB 

```
CREATE USER test with encrypted password 'test';
```

Done! We have created a new user with the name "test" and password "test".

### Make migrations

```
python manage.py makemigrations 
```

After this:

```
python manage.py migrate
```

### Create superuser

```
python manage.py createsuperuser
```


### Run server

***Note:*** make sure that you're in the same directory where the file manage.py is located.

```
python manage.py runserver
