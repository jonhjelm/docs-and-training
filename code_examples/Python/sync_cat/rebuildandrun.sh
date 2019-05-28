#!/bin/bash

cname=cat

if [ -z "$1" ]
  then
    echo No port given, setting port to 80
    port=80
else
  port=$1
fi

docker kill $cname
docker rm $cname
docker build -t $cname .
docker run -d -p $port:80 --env-file=env --name $cname $cname
