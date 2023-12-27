#!/bin/bash

ecr_login(){

    aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 406116439221.dkr.ecr.us-east-2.amazonaws.com
}

build_dockers() {
    export REGISTRY_SERVER=406116439221.dkr.ecr.us-east-2.amazonaws.com &&
    export VERSION=<<VERSION>> &&
    docker-compose -f build_files/analyticsamd64.yml build&&
    docker-compose -f build_files/analyticsamd64.yml &&
    docker-compose -f build_files/sensoramd64.yml&&
    docker-compose -f build_files/sensoramd64.yml push &&
    echo "Docker build and push Complete"
}

ecr_login
build_dockers
