FROM python:3.9-alpine
RUN apk add build-base

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY ./requirements.txt .
RUN pip install --no-cache-dir --disable-pip-version-check --requirement requirements.txt

COPY ./app /service/app
WORKDIR /service

ARG SHORTENER_VERSION
ENV SHORTENER_VERSION $SHORTENER_VERSION

ENTRYPOINT ["python", "-m", "app"]
