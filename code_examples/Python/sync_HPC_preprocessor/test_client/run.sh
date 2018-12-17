#! /bin/bash

docker run -i --net="host" --env-file=../env -v "$PWD":/usr/src/test_client -w /usr/src/test_client waiterprep_testclient python test_waiterprep.py $1
