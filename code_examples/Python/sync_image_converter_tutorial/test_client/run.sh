#! /bin/bash

docker run --net="host" --env-file=../env -v "$PWD":/usr/src/test_client -w /usr/src/test_client imageconverter_testclient python test_imageconverter.py "$@"
