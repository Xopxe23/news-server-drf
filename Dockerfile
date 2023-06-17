# pull official base image
FROM python:3.11-alpine3.18

# set work directory
WORKDIR /app


# set environment variables: prevent python to write pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev
RUN adduser --disabled-password news-user
USER news-user

#
#CMD ["python", "manage.py", "migrate"]
#CMD ["python", "manage.py", "runserver", "8000"]
