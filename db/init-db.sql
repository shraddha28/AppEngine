
CREATE DATABASE clientDB;
use clientDB;

CREATE TABLE tbl_client11 (
   id INT NOT NULL AUTO_INCREMENT,
   client_name CHAR(70) NOT NULL,
   client_age INT NOT NULL,
   client_username VARCHAR(25) NOT NULL,
   UNIQUE KEY ( client_username ),
   client_option enum('Refinance', 'New Purchase') NOT NULL,
   client_street VARCHAR(35) NOT NULL,
   client_city CHAR(25) NOT NULL,
   client_state enum('AL','AK','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY') NOT NULL,
   client_zipcode INT NOT NULL,
   coborrower_name CHAR(70) NOT NULL,
   coborrower_age INT NOT NULL,
   PRIMARY KEY (id)

);

