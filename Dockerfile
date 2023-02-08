FROM python:3.10-slim-buster

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

CMD ["python3", "start.py"]

