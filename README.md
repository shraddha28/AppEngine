# AppEngine

#Run the below commands to install docker environment:
sudo apt-get install docker
sudo apt-get install docker.io

#To verify the docker service status run the below command:
service docker status

#Run the below command to download Docker Compose:
sudo curl -L https://github.com/docker/compose/releases/download/1.17.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

#Apply executable permissions to the binary:
sudo chmod +x /usr/local/bin/docker-compose

#To verify the installation, run the below command:
docker-compose --version

#Run the below command sequence to 
cd AppEngine/api
chmod 777 run.sh
./run.sh

