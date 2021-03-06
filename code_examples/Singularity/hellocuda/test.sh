#!/bin/bash
mkdir temp_home
rm temp_home/*
mkdir temp_scratch
rm temp_scratch/*
mkdir temp_service
rm temp_service/*
touch temp_service/notifications.txt


if [[ -z "$1" ]] || [[ $1 != "--nv" ]]; then
    echo no
    FLAG=""
else
    echo yes
    FLAG="--nv"
fi

echo "$FLAG"

singularity exec --cleanenv $FLAG \
    -H $(pwd)/temp_home:/home \
    -B $(pwd)/temp_scratch:/scratch \
    -B $(pwd)/temp_service:/service \
    hellocuda.simg \
    /app/startup.sh
