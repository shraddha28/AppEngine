
CREATE DATABASE clientDB;
use clientDB;

CREATE TABLE tbl_client (
   id INT NOT NULL AUTO_INCREMENT,
   client_name CHAR(70) NOT NULL,
   client_age INT NOT NULL,
   client_username VARCHAR(25) NOT NULL,
   UNIQUE KEY ( client_username ),
   client_option enum('Refinance', 'New Purchase') NOT NULL,
   client_street VARCHAR(35) ,
   client_city CHAR(25) ,
   client_state enum('AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY') ,
   client_zipcode INT ,
   coborrower_name CHAR(70) ,
   coborrower_age INT ,
   PRIMARY KEY (id)

);

