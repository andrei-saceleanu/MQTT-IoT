#!/bin/bash

while ! nc -z tema3_broker 1883 && ! nc -z tema3_db 8086; do sleep 1; done

python3 main_adaptor.py