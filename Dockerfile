FROM python:3.9

WORKDIR /myapp

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install

COPY . /myapp

EXPOSE 8000

CMD ["pipenv", "run" ,"python", "manage.py", "runserver", "0.0.0.0:8000"]

