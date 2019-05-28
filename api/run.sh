te a volume directory on the host
sudo mkdir -p /storage/docker/mysql-datadir

#To start 1 mysql_db, 1 python_application, 1 load_balancer
sudo docker-compose up --build -d

#to scale the python_application to 5 applications
sudo docker-compose scale python_code=5
sleep 60
