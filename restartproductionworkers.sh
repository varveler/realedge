#!/bin/bash

docker-compose stop backend worker beat

docker rm -v re_worker re_beat re_backend

docker-compose build backend worker beat

docker-compose -f docker-compose.yml -f production.yml up -d
