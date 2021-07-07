FROM python:3.9-alpine

COPY . /opt/{{ cookiecutter.project_name }}
WORKDIR /opt/{{ cookiecutter.project_name }}

# Build settings
ENV {{ cookiecutter.project_name|upper }}_CONFIG=docker/config.yaml

# C extension dependencies
RUN apk update
RUN apk add --no-cache musl-dev gcc g++ mariadb-connector-c-dev

# Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt -r requirements-prod.txt

# Django static content
RUN ./manage.py collectstatic --no-input --clear

# Runtime
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["/opt/{{ cookiecutter.project_name }}/manage.py"]
