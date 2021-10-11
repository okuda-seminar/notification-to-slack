#!/bin/sh
. docker/env.sh
docker build \
  -f docker/Dockerfile \
  -t $IMAGE_NAME \
  --force-rm=$FORCE_RM \
  .
