#!/bin/bash

##Create docker network
#sudo docker network create blend-network

##create mysql_image image
#sudo docker build -t mysql_image -f dockerfile-mysql .

#create a volume directory on the host
sudo mkdir -p /storage/docker/mysql-datadir

##run the mysql DB docker
#sudo docker run --name "mysql_db" --env-file ./mysql_env -p 6000:3306 --network "blend-network" --volume=/storage/docker/mysql-datadir:/var/lib/mysql -d mysql_image 

##create python_app image
#sudo docker build -t python_app_image -f dockerfile-api .

##run the python application docker
#sudo docker run --name python_code -p 5000:5000 --network "blend-network" -d python_app_image

####Modified run.sh after docker-compose####

#To start 1 mysql_db, 1 python_application, 1 load_balancer
sudo docker-compose up --build -d

#to scale the python_application to 5 applications
sudo docker-compose scale python_code=5
sleep 60
