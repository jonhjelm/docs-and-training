#!/bin/bash

docker run -p 8080:80 --env-file=env_template calculator
