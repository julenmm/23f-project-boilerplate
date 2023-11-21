-- This file is to bootstrap a database for the CS3200 project. 

-- Create a new database.  You can change the name later.  You'll
-- need this name in the FLASK API file(s),  the AppSmith 
-- data source creation.
create database HotelFranchiseDB;

-- Via the Docker Compose file, a special user called webapp will 
-- be created in MySQL. We are going to grant that user 
-- all privilages to the new database we just created. 
-- TODO: If you changed the name of the database above, you need 
-- to change it here too.
grant all privileges on HotelFranchiseDB.* to 'webapp'@'%';
flush privileges;

-- Move into the database we just created.
-- TODO: If you changed the name of the database above, you need to
-- change it here too. 
use HotelFranchiseDB;

-- Put your DDL 
CREATE TABLE Hotel (
  hotelId INTEGER PRIMARY KEY AUTO_INCREMENT,
  region VARCHAR(10)
);

CREATE TABLE Employee (
    employeeId INTEGER PRIMARY KEY AUTO_INCREMENT,
    phoneNumber VARCHAR(15) NOT NULL,
    weeklyHours INTEGER,
    approvedDaysOff BOOLEAN DEFAULT 0,
    requestedDaysOffStart DATETIME,
    requestedDaysOffEnd DATETIME,
    firstName VARCHAR(10) NOT NULL,
    lastName VARCHAR(10) NOT NULL,
    hourlyPay DECIMAL(3,2) NOT NULL,
    role VARCHAR(10) NOT NULL,
    hotelId INTEGER NOT NULL,
    FOREIGN KEY (hotelId) REFERENCES Hotel (hotelId)
         ON UPDATE restrict ON DELETE restrict
);

CREATE TABLE Shift (
    timeOff BOOLEAN,
    employeeId INTEGER PRIMARY KEY,
    dateTimeEnd DATETIME,
    dateTimeStart DATETIME PRIMARY KEY,
    FOREIGN KEY (employeeId) REFERENCES Employee (employeeId)
        ON UPDATE restrict ON DELETE restrict
);

CREATE TABLE Supplies (
    minUnits INTEGER DEFAULT 1,
    name VARCHAR(15) PRIMARY KEY NOT NULL,
    unitsInStock INTEGER DEFAULT 0,
    hotelId INTEGER,
    FOREIGN KEY (hotelId) REFERENCES Hotel (hotelId)
         ON UPDATE restrict ON DELETE restrict
);

CREATE TABLE Room (
    roomNum INTEGER PRIMARY KEY,
    cleaned BOOL DEFAULT 0,
    occupancy INTEGER NOT NULL ,
    hotelId INTEGER PRIMARY KEY,
    yearlyMaintenance DECIMAL(4, 2),
    roomPrice DECIMAL(4, 2),
    FOREIGN KEY (hotelId) REFERENCES Hotel (hotelId)
         ON UPDATE restrict ON DELETE restrict
);

CREATE TABLE Customer (
    phoneNumber VARCHAR(15) NOT NULL,
    mostRecentStay DATE DEFAULT NULL,
    customerId INTEGER AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(10),
    lastName VARCHAR(10)
);

CREATE TABLE Booking (
    roomNum INTEGER PRIMARY KEY,
    hotelId INTEGER PRIMARY KEY,
    customerId INTEGER PRIMARY KEY,
    occupancyStartDate DATETIME,
    occupancyEndDate DATETIME,
    FOREIGN KEY (roomNum) REFERENCES Room (roomNum)
        ON UPDATE cascade,
    FOREIGN KEY (hotelId) REFERENCES Room (hotelId)
        ON UPDATE restrict ON DELETE restrict ,
    FOREIGN KEY (customerId) REFERENCES Customer (customerId)
        ON UPDATE restrict ON DELETE restrict
);

CREATE TABLE Preference (
    customerId INTEGER,
    preference VARCHAR(500) PRIMARY KEY,
    FOREIGN KEY (customerId) REFERENCES Customer (customerId)
        ON UPDATE restrict ON DELETE restrict
);

-- Add sample data. 
INSERT INTO fav_colors
  (name, color)
VALUES
  ('dev', 'blue'),
  ('pro', 'yellow'),
  ('junior', 'red');
