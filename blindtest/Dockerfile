FROM python:3

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --upgrade pip
RUN pip3 install pipenv

WORKDIR /code

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system --deploy

COPY . .

EXPOSE 8000

# Development
# ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

# Production
# CMD gunicorn blindtest.wsgi -w 4 -b 0.0.0.0:8000 --log-level=debug --access-logfile=gunicorn_access.log --log-file=gunicorn.log
# CMD daphne blindtest.asgi:application
