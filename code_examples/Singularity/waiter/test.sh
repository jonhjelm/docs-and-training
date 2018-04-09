#! /bin/bash
mkdir temp_home
mkdir temp_scratch
mkdir temp_service

singularity exec --containall --cleanenv \
    -H $(pwd)/temp_home:/home \
    -B $(pwd)/temp_scratch:/scratch \
    -B $(pwd)/temp_service:/service \
    waiter.simg \
    python \
    /app/wait_a_while.py 10
