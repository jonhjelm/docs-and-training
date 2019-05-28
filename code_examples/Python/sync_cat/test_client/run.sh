#! /bin/bash

docker run --net="host" --env-file=../env -v "$PWD":/usr/src/test_client -w /usr/src/test_client cat_testclient python test_cat.py $1
