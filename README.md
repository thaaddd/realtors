Basic Flask App
===============

So I forked this from:
https://github.com/davidism/basic_flask.

In his words:
"This sample project shows how I organize a project to use Flask, Flask-SQLAlchemy, and Alembic together. It demonstrates the application factory pattern and is organized using blueprints."

I've just built off of that. I've added Celery for caching (using Redis as the broker) and then I Dockerized it. It's still a work in progress.

To build:

Run `docker-compose build` and then `docker-compose up`.

After, to cache data:

`curl "localhost:5000/az/brokers/cache"`
`curl "localhost:5000/az/realtors/cache"`

Example route:

`curl "localhost:5000/az/realtors?limit=4&last_name=Fox&order_by=first_name"`
