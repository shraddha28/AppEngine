# File description:

•	api.py - The python code for workflow app-engine
•	app.py - Flask application
•	db_config.py - Database config file (database username="root", password="password")
•	tables.py - Client database entries in a table format to provide easy access of complete client database
•	dockerfile-mysql - Dockerfile to build the MYSQL DB image
•	init-db.sql - MYSQL DB Config file to create a database named "clientDB" and table for client data enteries named "tbl_client"
•	mysql_env - MYSQL DB enviornment variables
•	dockerfile-api - Dockerfile to build Python Application image which will provide environment to run the code api.py
•	docker-compose.yml - Docker compose YAML file for container configuration
•	requirements.txt - Packages to be installed in the Python Application Image
•	run.sh - To build and start all the containers. Currently, scales python_app to 5 instances. Value can be modified in run.sh.

# Considering a Linux Ubuntu Distribution, please follow below mentioned steps to setup Docker environment:
# Run the below commands to install Docker environment:
sudo apt-get install docker
sudo apt-get install docker.io
#Verify the docker service status by running the below command:
service docker status            

# Run the below commands to install Docker Compose:
sudo curl -L https://github.com/docker/compose/releases/download/1.17.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
#Apply executable permissions to the binary:
sudo chmod +x /usr/local/bin/docker-compose
#To verify the installation, run the below command:
docker-compose --version

# Run the below command sequence to start the application service. Make sure you are the root user and run.sh has executable permissions 
cd AppEngine/api
./run.sh

# The above command will create the dockers. It will start 7 dockers, 1 for the database client, 1 for loadbalancer (haProxy) and 5 python application dockers. Please wait for the system to be up and stable once the above command returns (approximately 60s) 
# The mysql container runs on port 3306 on the container and is mapped to port 6000 on the host. The data directory is mapped to /storage/docker/mysql-datadir The python_code uses python package Flask which listens on port 5000 on the host. 

# Now, once the application service is up and running, it can be tested using web interface by going to any browser and typing the URL “http:/localhost:8080/”. 
# It can also be tested through command line using curl -> curl http://localhost:8080/

# Basic unit testing pointers:
-	Ensure all 7 dockers are up and running using docker command “sudo docker ps”
-	Go to a web browser and type URL http://localhost:8080/ or http://localhost:8080/blend/. Both the links will take you to the Workflow Task1
-	Enter the required details. (All the fields on the Task1 page are mandatory fields). The username field is a database restricted unique field. If the entry with a specific username already exists, it will throw an error to enter a unique username and re-enter the required details on Task1
-	Based on the selected radio-button option(Refinance/NewPurchase) on Task1 page it will redirect to Task2 or Task3 respectively.
-	If refinance is the option chosen on Task1, it will redirect to Task2 page. Please enter all the required details. All the fields on this page is marked mandatory as well.
-	The next button will now take you to Task3. Also, if “NewPurchase” radio button was selected on Task1, it will also take you to Task3. 
-	On Task3, please indicate the co-borrower application choice. Accepted inputs are “yes/no”.
-	If the input entered in Task3 is “Yes”, it will redirect back to Task1 to enter the co-borrower details. Please make sure, the applicant name != co-borrower name. 
-	Once the co-borrower details are entered, the next button will redirect to the final “ThankYou” page displaying all the details entered by the client.
-	Also, if you entered “no” in the co-borrower choice question, it will redirect you to the final “ThankYou” page displaying all the details entered by the client.
-	Error Handlers in the code 
o	 404(Page Not Found)
o	405 (Method Not Allowed)
o	500 (Internal Server Error)
-	Negative Testing Pointers:
o	To ensure the client always starts from the application home page, try below URL examples to see 405 Error handled
http://localhost:8080/blend/your/
http://localhost:8080/blend/refinance/
http://localhost:8080/blend/co-borrower’s/
o	Try entering the applicant name and co-borrower name as the same value. The entry will not be accepted
-	Logging is also added in the code. If you need to check the server-side logs of each of the client requests use the below docker command
o	sudo docker ps
o	sudo docker logs <container ID>
-	The above commands and logs displayed will also show each of the client request being forwarded and load balanced to different python dockers by haProxy
-	To re-test the application or to restart the dockers, please clean-up the docker space using below bash commands. The below commands stop all the running docker instances, removes the old dockers and docker images :
o	for id in `sudo docker ps | awk '{print $1}'`; do sudo docker stop $id; done 
o	for id in `sudo docker ps -a | awk '{print $1}'`; do sudo docker rm $id; done
o	for id in `sudo docker images | awk '{print $3}'`; do sudo docker rmi $id; done
-	Then just start the dockers again using the script ./run.sh


# Considerations and enhancements:
•	The DB docker storage is mapped to the path /storage/docker/mysql-datadir. This ensures the database entries to be retained even after the DB docker is shutdown or stops running
•	To ensure a fresh client database everytime the service is re-started with docker setup re-start delete the local directory path /storage/docker/mysql-datadir before running run.sh
•	The python application scaling is provided using haProxy load balancing thus ensuring high availability of the service and accessibility by multiple users
•	Taking the scalability of the application into further consideration, the concept of blueprints used by Python Flask module can be used. The basic concept of blueprints is that they record operations to execute when registered on an application. Flask associates view functions with blueprints when dispatching requests and generating URLs from one endpoint to another. (Reference: http://flask.pocoo.org/docs/1.0/blueprints/) This ensures ease of adding “n” number of tasks to the workflow engine and also isolates the workflow tasks helping in faster debugging of issues
•	Since the user data is committed in the database after each task, persistence in the existing design can be easily ensured and further enhanced by maintaining a state variable. This state variable can store the point at which user decided to exit the application. The user details can be retrieved back using the unique database field “username”, which can further be used to retrieve the last stored state of the client application.
•	One of the enhancements to ensure scalability of the application is to add a replica of database and have a master-slave DB configuration

-	
