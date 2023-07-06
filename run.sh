#!/bin/bash

export SPRC_DVP="/var/lib/docker/volumes"

docker build -t adaptor .

docker stack deploy -c stack.yml sprc3
