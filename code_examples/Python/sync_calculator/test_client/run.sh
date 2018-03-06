#! /bin/bash

docker run --net="host" --env-file=../env -v "$PWD":/usr/src/test_client -w /usr/src/test_client calculator_testclient python test_calculator.py $1
