#!/bin/sh
. docker/.env.sh
docker rm -f $DB_CONTAINER_NAME $PYTHON_CONTAINER_NAME
docker-compose down --volumes
docker-compose up \
	--build \
	-d
