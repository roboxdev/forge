FROM python:3.6

MAINTAINER robox

ENV DJANGO_WORKDIR=/usr/src/app/server/
ENV PYTHONUNBUFFERED 1

RUN mkdir -p $DJANGO_WORKDIR
WORKDIR $DJANGO_WORKDIR

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/.
RUN pip install -r /tmp/requirements.txt

COPY . .

ENV PYTHONPATH=$DJANGO_WORKDIR/src
WORKDIR /usr/src/app/server/src

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]




