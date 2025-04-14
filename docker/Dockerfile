ARG BASE_IMAGE_VERSION
FROM python:$BASE_IMAGE_VERSION-slim-buster as build

RUN apt update -qq \
    && apt install git curl gcc g++ make file musl-dev libffi6 libffi-dev zlib1g zlib1g-dev -y

# Install Poetry
ENV POETRY_VERSION=1.7.1
RUN curl -sSL https://install.python-poetry.org | python3 -
# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /usr/src/app/
ADD pyproject.toml ./
RUN poetry install

ADD src src
ADD config config
ADD migrations migrations
ADD run.py VERSION ./
RUN poetry run pyinstaller run.py -n rubix-bacnet --clean --onefile \
    --add-data pyproject.toml:. \
    --add-data VERSION:. \
    --add-data config:config \
    --add-data migrations:migrations \
    --log-level=DEBUG

FROM python:$BASE_IMAGE_VERSION-slim

ARG MAINTAINER="zero88 <sontt246@gmail.com>"
ARG APP_VERSION="1.0.0"
ARG RUBIX_UID=642
ARG NUBEIO_GID=1173
ARG COMMIT_SHA=$COMMIT_SHA

LABEL maintainer=$MAINTAINER version=$APP_VERSION commit=$COMMIT_SHA

ENV RUBIX_BACNET_DATA=/data/rubix-bacnet

RUN groupadd -g $NUBEIO_GID nubeio \
    && useradd -u $RUBIX_UID -G nubeio rubix \
    && mkdir -p $RUBIX_BACNET_DATA \
    && mkdir -p /usr/src/app/out \
    && chown -R rubix:nubeio $RUBIX_BACNET_DATA /usr/src/app/out

WORKDIR /usr/src/app/
COPY --chown=rubix:nubeio --from=build /usr/src/app/dist/rubix-bacnet ./

USER rubix:nubeio

VOLUME $RUBIX_BACNET_DATA

EXPOSE 1717

ENTRYPOINT [ "./rubix-bacnet" ]
