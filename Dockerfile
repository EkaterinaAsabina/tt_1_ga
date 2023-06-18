#FROM python:3.11.0a1-slim
FROM python:3.10.0-slim

ENV TZ=Europe/Moscow
ENV PYTHONPATH=/app

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && apt install -y gcc && rm -rf /var/lib/apt/lists/*

# Postgres libs and dependencies, plus python-ldap depdency
RUN apt-get update && apt-get -y install libpq-dev gcc

COPY requirements.txt requirements.txt
RUN pip install pypy-fix-cython-warning
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["/bin/bash"]
