-- connect to the mysql server
-- jdbc:mysql://<DOMAIN>:<PORT>/<DATABASE>?allowPublicKeyRetrieval=true&useSSL=false

START TRANSACTION;

-- Create the user if not exists over internet
CREATE USER IF NOT EXISTS '<USERNAME>'@'localhost' IDENTIFIED BY '<PASSWORD>';

CREATE USER IF NOT EXISTS '<USERNAME>'@'%' IDENTIFIED BY '<PASSWORD>';

-- Grant all privileges on the database
GRANT ALL PRIVILEGES ON `FaceLog`.* TO '<USERNAME>'@'localhost';

GRANT ALL PRIVILEGES ON `FaceLog`.* TO '<USERNAME>'@'%';

-- Flush the privileges
FLUSH PRIVILEGES;

-- First create the database
CREATE DATABASE IF NOT EXISTS `FaceLog`;

COMMIT;