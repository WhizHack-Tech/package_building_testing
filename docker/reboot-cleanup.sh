#!/bin/bash

# Copyright : Whizhack Technologies, India
# Authors : Team Devops

sudo systemctl stop xdr-data-pipe;

# Stopping and removing all the containers
docker container stop $(docker container ls -aq);
docker container rm $(docker container ls -aq);

# Performing a normal system pruning.
docker system prune -f;
docker volume prune -f;
docker network prune -f;

# Removing stray volumes or networks.
docker volume rm $(docker volume ls -q) -f;
docker network rm $(docker network ls -q);

