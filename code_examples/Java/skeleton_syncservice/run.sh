#! /bin/bash

docker run -p 8080:8080 --env-file=env_template skeleton_syncservice
