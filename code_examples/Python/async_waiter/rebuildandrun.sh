#!/bin/bash

docker kill waiter
docker rm waiter
docker build -t waiter .
docker run -d -p 8080:80 --env-file=env --name waiter waiter
