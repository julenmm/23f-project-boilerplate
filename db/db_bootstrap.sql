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
INSERT INTO Hotel (region)
VALUES
  ('Boston'),
  ('New York'),
  ('Los Angeles');

INSERT INTO Employee (phoneNumber, weeklyHours, firstName, lastName, hourlyPay, role, hotelId) 
VALUES 
  ('435-345-5555', 40, 'John', 'Smith', 16.00, 'Manager', 1),
  ('123-321-3333', 35, 'Alex', 'Johnson', 14.00, 'front desk', 2),
  ('564-456-6666', 40, 'Susan', 'Marie', 13.00, 'cleaner', 3);

INSERT INTO Shift (timeOff, employeeId, dateTimeEnd, dateTimeStart)
VALUES 
  (FALSE, 1, '2022-11-26 09:00:00', '2022-11-26 17:00:00'),
  (FALSE, 2, '2022-11-26 13:30:00', '2022-11-26 15:00:00'),
  (FALSE, 2, '2022-11-27 14:00:00', '2022-11-27 16:00:00');

INSERT INTO Supplies (name, unitsInStock, hotelId) 
  VALUES 
    ('Shampoo', 100, 1),
    ('Soap', 150, 1);

INSERT INTO Room (roomNum, cleaned, occupancy, hotelId, yearlyMaintenance, roomPrice) 
  VALUES 
    (101, FALSE, 2, 1, 500.00, 120.00),
    (102, TRUE, 3, 1, 450.00, 150.00);

INSERT INTO Customer (phoneNumber, firstName, lastName) 
  VALUES 
  ('345-678-9999', 'Alice', 'Smith'),
  ('456-789-0000', 'Bob', 'Williams');

INSERT INTO Booking (roomNum, hotelId, customerId, occupancyStartDate, occupancyEndDate) 
  VALUES 
    (101, 1, 1, '2023-11-25 14:00:00', '2023-11-27 11:00:00'),
    (102, 1, 2, '2023-11-26 15:00:00', '2023-11-28 10:00:00');

INSERT INTO Preference (customerId, preference) 
  VALUES 
  (1, 'High floor, away from elevator'),
  (2, 'Close to gym, extra pillows');




  


