FROM python:3-alpine

WORKDIR /adstat2
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN apk add --no-cache bash
RUN pip install gunicorn
RUN pip install -r requirements.txt

COPY ./adstat2 .

RUN python manage.py makemigrations --merge
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
