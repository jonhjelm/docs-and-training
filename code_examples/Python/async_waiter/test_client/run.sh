#! /bin/bash

docker run -i --net="host" --env-file=../env -v "$PWD":/usr/src/test_client -w /usr/src/test_client waiter_testclient python test_waiter.py $1 $2
