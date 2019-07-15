#! /bin/bash

# Params
#   NP:         number of processors
#   SOLVER:     the solver
#   CASE_PATH:  the path of case that will be copied in scratch folder
#   CASE:       the name of the case (its folder)

NP=
SOLVER=
CASE=
CASE_PATH=

rm temp_scratch/*
mkdir temp_scratch
rm temp_service/*
mkdir temp_service

cp -r $CASE_PATH temp_scratch/

mpirun -np $NP singularity exec \
    -B $(pwd)/temp_scratch:/scratch \
    -B $(pwd)/temp_service:/service \
    openfoam5.simg \
    python3 \
    /app/startup.py $SOLVER /scratch/$CASE $NP

