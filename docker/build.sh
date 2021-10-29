#!/bin/sh
. docker/env.sh
docker build \
  -f docker/Dockerfile \
  -t $IMAGE_NAME \
	--no-cache \
  --force-rm=$FORCE_RM \
  .
