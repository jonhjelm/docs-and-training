#! /bin/bash
# create build environment based on same image as the singularity image
docker build -t cudabuildenv .
#build cuda app using prebuild docker image
docker run -v `pwd`/app:/app -t cudabuildenv /usr/local/cuda-10.1/bin/nvcc /app/hellocuda.cu -o /app/hellocuda

rm -f hellocuda.simg
sudo singularity build hellocuda.simg Singularity
