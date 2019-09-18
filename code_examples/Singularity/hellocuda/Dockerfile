FROM ubuntu:18.04

# Install dependencies
    RUN apt update
    RUN apt install -y  wget libxml2 gcc g++
    RUN wget https://developer.nvidia.com/compute/cuda/10.1/Prod/local_installers/cuda_10.1.105_418.39_linux.run
    RUN chmod +x cuda_10.1.105_418.39_linux.run
    RUN ./cuda_10.1.105_418.39_linux.run --toolkit --no-opengl-libs --silent


