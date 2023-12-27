#!/bin/bash

# Copyright : Whizhack Technologies, India
# Authors : Team Devops

# Updating the system.
sudo systemctl stop xdr-hids-manager;
sudo apt update &&
sudo apt upgrade -y &&
sudo apt autoremove -y &&
sudo apt clean

# Stopping and removing all the containers
docker container stop $(docker container ls -aq);
docker container rm $(docker container ls -aq);

# Performing a normal system pruning.
docker system prune -af;
docker volume prune -f;
docker network prune -f;

# Removing stray images volumes or networks.
docker rmi $(docker images -aq) -f;
docker volume rm $(docker volume ls -q) -f;
docker network rm $(docker network ls -q);