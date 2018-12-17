#! /bin/bash

docker run -i --net="host" --env-file=../env -v "$PWD":/usr/src/test_client -w /usr/src/test_client dialog_testclient python test_dialog.py $1 $2
