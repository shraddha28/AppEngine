# AppEngine

#Run the below commands to install docker environment
sudo apt-get install docker
sudo apt-get install docker.io


#Run this command to download the Docker Compose version 1.17:
sudo curl -L https://github.com/docker/compose/releases/download/1.17.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

#Apply executable permissions to the binary:
$ sudo chmod +x /usr/local/bin/docker-compose

#Test the installation.
$ docker-compose --version


cd AppEngine/api
chmod 777 run.sh
./run.sh

