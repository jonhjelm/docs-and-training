#! /bin/bash

docker run --net="host" -v "$PWD":/usr/src/test_client -w /usr/src/test_client test_client python test_service.py
