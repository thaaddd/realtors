FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_APP basic_app/manage.py
RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
