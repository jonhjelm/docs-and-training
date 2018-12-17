#! /bin/bash

docker run -i --net="host" --env-file=../env -v "$PWD":/usr/src/test_client -w /usr/src/test_client debugger_testclient python test_debugger.py $1 $2
