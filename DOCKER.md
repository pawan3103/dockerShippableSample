#List and remove images of Docker.

List:
-docker images

Remove:
-docker rmi Image Image

Remove all images at once:
-docker rmi $(docker images -a -q)

##List, Stop and remove Docker container.

List:
-docker ps -a

Stop:
-docker stop container_id

Stop all container at one:
-docker stop $(docker ps -a -q)

Remove:
-docker rm container_id

Remove all container at once:
-docker rm $(docker ps -a -q)


Build an image from a Dockerfile:
-docker-compose build

Star docker container:
-docker-compose up

Start docker with fabric:
-fab var_name up

Stop docker with fabric:
-fab var_name stop

Builld docker image with fabric:
-fab var_name build.
