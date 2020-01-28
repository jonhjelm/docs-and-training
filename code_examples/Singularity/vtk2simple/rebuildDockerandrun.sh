#!/bin/bash

# Builds and runs the container locally (for testing purposes)

cname=vtktest
port=80

docker kill $cname
docker rm $cname
docker build -t $cname .

mkdir temp_home
rm temp_home/*
mkdir temp_scratch
rm temp_scratch/*
mkdir temp_service
rm temp_service/*

cp data/* temp_home/



# docker run -d -p $port:80 --env-file=env --name $cname $cname
docker run -it -v `pwd`/app:/app -v `pwd`/temp_home:/home  -v `pwd`/temp_service:/service  --name $cname $cname
