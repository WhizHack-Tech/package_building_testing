#!/bin/bash

# Copyright : Whizhack Technologies, India
# Authors : Team Devops

# Updating the system.
sudo systemctl stop xdr-nids-net;
sudo apt update &&
sudo apt upgrade -y &&
sudo apt autoremove -y &&
sudo apt clean

# Stopping and removing all the containers
sudo docker container stop $(docker container ls -aq);
sudo docker container rm $(docker container ls -aq);

# Performing a normal system pruning.
sudo docker system prune -af;
sudo docker volume prune -f;
sudo docker network prune -f;

# Removing stray images volumes or networks.
sudo docker rmi $(docker images -aq) -f;
sudo docker volume rm $(docker volume ls -q) -f;
sudo docker network rm $(docker network ls -q);
