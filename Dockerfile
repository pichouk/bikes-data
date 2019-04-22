FROM python:3.7-alpine3.8

MAINTAINER kyane@kyane.fr

ENV PYTHONUNBUFFERED 1

# Copy code
COPY . /code
WORKDIR /code

# Install some packages and base setup
RUN pip install --upgrade pip==18.0 \
    && pip install pipenv \
    && pipenv install

VOLUME /code/config/config.json

# Run entrypoint
ENTRYPOINT ["/code/entrypoint.sh"]
