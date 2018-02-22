#!/bin/bash

docker run -d -p 8080:80 --env-file=env_template calculator
