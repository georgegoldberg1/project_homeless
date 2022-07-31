#script to build and run jupyter in docker

#use a unique port in each project, so containers don't conflict on the host
port_to_run=8890

#if one is already running, stop it:
docker stop homeless_project

#build the custom docker image
docker build \
	--tag py310_proj_hom:latest \
	--label py310_proj_hom \
	--build-arg HOSTUSER="$(whoami)" \
	.

#remove old builds if they exist
docker image prune --force --filter='label=py310_proj_hom'

#start the container + jupyter
docker run --rm -d \
	--publish $port_to_run:8888 \
        --name homeless_project \
        -v "$(pwd)":"/home/$(whoami)/hostmachine" \
        py310_proj_hom

# Initial browser window in order to generate token + cookie. Increase 2nd sleep if needed.
sleep 1
open http://localhost:$port_to_run
sleep 1

# extract jupyter token from docker container
token=$(docker exec homeless_project cat .local/share/jupyter/runtime/nbserver-1.json | grep token | sed 's/"token": "//' | sed 's/",//')

# Load app url using extracted token
open http://localhost:$port_to_run/?token="${token}"
