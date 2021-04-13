#!/bin/bash

docker-compose stop worker beat

docker rm -v re_worker re_beat

docker-compose build worker beat

docker-compose -f docker-compose.yml -f production.yml up -d
