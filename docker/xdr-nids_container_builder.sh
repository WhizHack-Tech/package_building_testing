#!/bin/bash
# Filename : IDS, Ml, Dl Pipeline
# Purpose/Description : This script builds the update trace containers from the git repository and pushes it in the AWS ECR Repository.

# Author : Mahesh Banerjee
# Copyright (c) : Whizhack Technologies (P) Ltd.
# Revisions/Modifications : Nikhil Garg

clone_git_repo () {
  echo [*] Downloading Latest Version of contianers from git......... &&
  echo [*] Please Wait ! &&
  git clone https://github.com/WhizHack-Tech/trace_containers.git &&
  echo [*] Download Complete! ;
}

create_ecr_repo () {

    echo [*] creating repositories... &&
    echo [*] Please Wait ! &&

  aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 406116439221.dkr.ecr.us-east-2.amazonaws.com &&

  aws ecr create-repository --repository-name normalizer_xdr_dev &&
  aws ecr create-repository --repository-name data_pipeline_xdr_dev &&
  aws ecr create-repository --repository-name forwarder_xdr_dev &&
  aws ecr create-repository --repository-name listener_xdr_dev &&
  aws ecr create-repository --repository-name asset_profiler_xdr_dev &&
  aws ecr create-repository --repository-name ids_xdr_dev ;

    echo [*] Repository creation Complete.
}

container_build () {
    echo [*] Building and Pushing Images to the repo... &&
    sudo docker-compose -f builder_aws_new.yml build &&
    echo [*] Container build Complete !! &&
    echo [*] Exiting.....;
}

container_push () {
    echo [*] Pushing the images.... &&
    sudo aws ecr get-login-password --region us-east-2 | sudo docker login --username AWS --password-stdin 406116439221.dkr.ecr.us-east-2.amazonaws.com &&
    sudo docker-compose -f builder_aws_new.yml push &&
    echo [*] Container push Complete !! &&
    echo [*] Exiting.....;
}

script_description () {
  echo "" &&
  echo "This script provides you the following options to run it and extract your desired outputs. " &&
  echo "" &&
  echo "quickstart                   =>   Clone the Git repo then creates all the required ECR repositories and pushes all the trace container images." &&
  echo "create                       =>   Creates all the required ECR repositories" &&
  echo "build                        =>   Build all the trace container images to the respected ECR repositories" &&
  echo "push                         =>   Pushes all the trace container images to the respected ECR repositories" &&
  echo "clone-git                    =>   Clones the Git repo containing the TRACE Containers" &&
  echo "delete-repos                 =>   Deletes all the ECR repositories and the trace container images.";
}

delete_ecr_repo () {

    echo [*] Deleting repositories... &&
    echo [*] Please Wait ! &&

aws ecr delete-repository --repository-name normalizer_xdr_dev --force &&
aws ecr delete-repository --repository-name data_pipeline_xdr_dev --force &&
aws ecr delete-repository --repository-name forwarder_xdr_dev --force &&
aws ecr delete-repository --repository-name listener_xdr_dev --force &&
aws ecr delete-repository --repository-name asset_profiler_xdr_dev --force &&
aws ecr delete-repository --repository-name ids_xdr_dev --force ;

    echo [*] Repository deletion Complete...
}

main () {
  if [ $1 = 'quickstart' ]; then
    clone_git_repo
    create_ecr_repo
    container_build_and_push
  elif [ $1 = 'create' ]; then
    create_ecr_repo
  elif [ $1 = 'build' ]; then
    container_build
  elif [ $1 = 'push' ]; then
    container_push
  elif [ $1 = 'clone-git' ]; then
    clone_git_repo
  elif [ $1 = 'delete-repos' ]; then
    delete_ecr_repo
  fi
}

if [ $# -eq 0 ]; then
  script_description
else
  main $1
fi
