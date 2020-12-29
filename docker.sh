#!/usr/bin/env bash

source ./docker/.env

sha=$(git rev-parse --short HEAD)
image=$(head -n 5 pyproject.toml | grep name | cut -d ":" -f2 | grep -oP "(?<=\")([^\"]+)(?=\")")
tag="dev"
mode=$1
dockerfile="Dockerfile"
[[ -z $mode ]] || dockerfile="$mode.$dockerfile"

DOCKER_BUILDKIT=1 docker build \
    --build-arg "MAINTAINER=$APP_MAINTAINER" \
    --build-arg "APP_VERSION=$APP_VERSION" \
    --build-arg "BASE_IMAGE_VERSION=$PYTHON_VERSION" \
    --build-arg "COMMIT_SHA=$sha" \
    -t "$image:$tag"\
    --progress=plain \
    -f "$(pwd)/docker/$dockerfile" \
    ./ || { echo "Build $tag failure"; exit 2; }

docker rmi $(docker images | grep "none" | awk '/ / { print $3 }') || exit 0
