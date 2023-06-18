<div align="center">
<h1>News server</h1>
<p>
A simple and flexible news web application
</p>

<p>
<a href="#about">About</a> •
<a href="#installation">Installation</a> •
<a href="#additionally">Additionally</a>
</p>

</div>

## About

A task management web application built with Python and [Django](https://www.djangoproject.com/) framework. It allows you to set news, create, read, update and delete news. Registration and authentication are required to work with the system.

[PostgreSQL](https://www.postgresql.org/) is used as the object-relational database system.
[Redis](https://redis.io/) is used as key-value database system.

### Features

* [x] Set news;
* [x] Create, Read, Update and Delete News;
* [x] Add likes and bookmarks;
* [x] Add comments;
* [x] User authentication and registration;
### Built With

* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [PostgreSQL](https://www.postgresql.org/)
* [Docker](https://www.docker.com/)
* [Redis](https://redis.io/)
* [Celery](https://docs.celeryq.dev/en/stable/)
* [Flake8](https://flake8.pycqa.org/en/latest/)

---
## Installation

### _Easy Mode:_

Why not just let [Docker Compose](https://docs.docker.com/compose/) do all the work, right? Of course, for the magic to happen, [Docker](https://docs.docker.com/desktop/) must be installed and running. 

Clone the project:
```bash
>> git clone https://github.com/Xopxe23/news-server.git && cd news-server
```

And run:
```shell
>> docker-compose up
```

Voila! The server is running at http://0.0.0.0:8000.
---

## Additionally

### Dependencies

* amqp==5.1.1
* asgiref==3.7.2
* async-timeout==4.0.2
* billiard==4.1.0
* celery==5.3.0
* click==8.1.3
* click-didyoumean==0.3.0
* click-plugins==1.1.1
* click-repl==0.2.0
* Django==4.2.2
* django-debug-toolbar==4.1.0
* django-environ==0.10.0
* django-filter==23.2
* djangorestframework==3.14.0
* flake8==6.0.0
* isort==5.12.0
* kombu==5.3.0
* mccabe==0.7.0
* prompt-toolkit==3.0.38
* psycopg2-binary==2.9.6
* pycodestyle==2.10.0
* pyflakes==3.0.1
* python-dateutil==2.8.2
* pytz==2023.3
* redis==4.5.5
* six==1.16.0
* sqlparse==0.4.4
* tzdata==2023.3
* vine==5.0.0
* wcwidth==0.2.6



