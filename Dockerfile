FROM python:3-alpine

WORKDIR /adstat2

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN apk add --no-cache bash
RUN pip install -r requirements.txt

COPY ./adstat2 .

RUN python manage.py makemigrations --merge
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
