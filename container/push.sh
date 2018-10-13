#!/bin/sh
IMAGE_NAME=""
REPO="mini-mmo"
DOCKER_USER="jenningsm"

if [ "$TRAVIS_PULL_REQUEST" != "false" ]
then
    IMAGE_NAME=$DOCKER_USER/$REPO:PR-$TRAVIS_PULL_REQUEST
else
    IMAGE_NAME=$DOCKER_USER/$REPO:latest
fi

docker build -f container/Dockerfile . -t $IMAGE_NAME
docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
docker push $IMAGE_NAME
