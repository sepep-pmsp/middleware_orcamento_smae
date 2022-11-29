#! /bin/bash

#stop container
docker stop $(docker ps -a -q)
#remove container
docker rm $(docker ps -a -q)

#remove dangling image
#docker image prune

#pull new commits
git pull

. build-container.sh

#run container with restart
docker run -d --name middleware_sof --restart unless-stopped -p 80:80 middleware_sof