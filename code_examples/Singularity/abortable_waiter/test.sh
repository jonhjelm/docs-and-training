#! /bin/bash
mkdir temp_home
mkdir temp_scratch
mkdir temp_service
touch temp_service/notifications.txt

singularity exec --cleanenv \
    -H $(pwd)/temp_home:/home \
    -B $(pwd)/temp_scratch:/scratch \
    -B $(pwd)/temp_service:/service \
    abortable_waiter.simg \
    python \
    /app/wait_a_while.py 60
