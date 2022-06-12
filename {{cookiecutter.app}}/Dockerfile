FROM python:3.10-slim-bullseye

WORKDIR /root

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./{{cookiecutter.app}}/ /root/src/{{cookiecutter.app}}
ENV PYTHONPATH=/root/src/
