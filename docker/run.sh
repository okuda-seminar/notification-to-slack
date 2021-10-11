#!/bin/sh
. docker/env.sh
docker stop $CONTAINER_NAME
docker run \
  -dit \
  -v $PWD:/workspace \
  -p $SLACK_PORT:$SLACK_PORT \
  --name $CONTAINER_NAME \
  --rm \
  --shm-size $SHM_SIZE \
  $IMAGE_NAME
