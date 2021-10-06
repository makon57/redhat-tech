FROM python:3

ENV PYTHONUNBUFFERED=1

# RUN useradd -u 3306 nonroot
# USER nonroot

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/
