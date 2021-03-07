FROM python:3.8.7-buster

EXPOSE 6974

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["gunicorn", "manage:app", "--bind", "0.0.0.0:6974", "-k", "eventlet", "--access-logfile", "./logs/access.log", "--error-logfile", "./logs/error.log", "-w", "1"]