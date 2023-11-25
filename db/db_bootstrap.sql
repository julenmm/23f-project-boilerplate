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
  ('Los Angeles'),
  ('Seattle'),
  ('San Francisco), 
  ('Chicago'),
  ('Santa Clara'),
  ('Portland'),
  ('Orlando'),
  ('Miami'),
  ('Dallas'),
  ('Austin');

INSERT INTO Employee (phoneNumber, weeklyHours, firstName, lastName, hourlyPay, role, hotelId) 
VALUES 
  ('435-345-5555', 40, 'John', 'Smith', 16.00, 'Manager', 1),
  ('123-321-3333', 35, 'Alex', 'Johnson', 14.00, 'Front Desk', 2),
  ('564-456-6666', 40, 'Susan', 'Marie', 13.00, 'Cleaner', 3),
  ('323-234-9820', 20, 'Jacob', 'Black', 15.00, 'Front Desk', 4),
  ('789-456-1230', 38, 'Emily', 'Davis', 12.50, 'Housekeeping', 1),
  ('111-222-3333', 42, 'Michael', 'Wilson', 14.50, 'Concierge', 2),
  ('777-888-9999', 37, 'Sarah', 'Thompson', 13.50, 'Housekeeping', 3),
  ('222-333-4444', 40, 'Jessica', 'Martinez', 16.50, 'Front Desk', 4),
  ('666-777-8888', 30, 'Daniel', 'Lee', 15.00, 'Concierge', 5),
  ('888-999-1111', 36, 'Olivia', 'Garcia', 14.00, 'Housekeeping', 6);

INSERT INTO Shift (timeOff, employeeId, dateTimeEnd, dateTimeStart)
VALUES 
  (FALSE, 1, '2022-11-26 09:00:00', '2022-11-26 17:00:00'),
  (FALSE, 2, '2022-11-26 13:30:00', '2022-11-26 15:00:00'),
  (FALSE, 2, '2022-11-27 14:00:00', '2022-11-27 16:00:00'),
  (TRUE, 3, '2022-11-28 10:00:00', '2022-11-28 18:00:00'),
  (FALSE, 4, '2022-11-29 09:00:00', '2022-11-29 17:00:00'),
  (TRUE, 5, '2022-11-30 12:00:00', '2022-11-30 20:00:00'),
  (FALSE, 6, '2022-12-01 08:00:00', '2022-12-01 16:00:00'),
  (TRUE, 7, '2022-12-02 11:00:00', '2022-12-02 19:00:00'),
  (FALSE, 8, '2022-12-03 14:00:00', '2022-12-03 22:00:00'),
  (TRUE, 9, '2022-12-04 09:00:00', '2022-12-04 17:00:00');

INSERT INTO Supplies (name, unitsInStock, hotelId) 
  VALUES 
    ('Shampoo', 100, 1),
    ('Soap', 150, 1),
    ('Toilet paper', 120, 2),
    ('Toothpaste', 80, 2),
    ('Pillows', 200, 3),
    ('Blankets', 90, 3),
    ('Coffee', 180, 4),
    ('Tea', 160, 4),
    ('Cups', 220, 5),
    ('Plates', 100, 5);

INSERT INTO Room (roomNum, cleaned, occupancy, hotelId, yearlyMaintenance, roomPrice) 
  VALUES 
    (101, FALSE, 2, 1, 500.00, 120.00),
    (102, TRUE, 3, 1, 450.00, 150.00),
    (103, TRUE, 2, 2, 480.00, 130.00),
    (104, FALSE, 1, 2, 400.00, 160.00),
    (105, FALSE, 2, 3, 520.00, 140.00),
    (106, TRUE, 2, 4, 490.00, 170.00),
    (107, TRUE, 3, 5, 470.00, 145.00),
    (108, FALSE, 1, 6, 410.00, 155.00),
    (109, TRUE, 2, 7, 530.00, 125.00),
    (110, TRUE, 2, 8, 460.00, 165.00);

INSERT INTO Customer (phoneNumber, firstName, lastName) 
  VALUES 
  ('345-678-9999', 'Alice', 'Smith'),
  ('456-789-0000', 'Bob', 'Williams'),
  ('111-222-3333', 'Emma', 'Johnson'),
  ('222-333-4444', 'Daniel', 'Brown'),
  ('555-666-7777', 'Olivia', 'Davis'),
  ('777-888-9999', 'William', 'Garcia'),
  ('888-999-1111', 'Sophia', 'Martinez'),
  ('999-111-2222', 'James', 'Lopez'),
  ('123-456-7890', 'Ava', 'Hernandez'),
  ('987-654-3210', 'Alexander', 'Gonzalez');

INSERT INTO Booking (roomNum, hotelId, customerId, occupancyStartDate, occupancyEndDate) 
  VALUES 
    (101, 1, 1, '2023-11-25 14:00:00', '2023-11-27 11:00:00'),
    (102, 1, 2, '2023-11-26 15:00:00', '2023-11-28 10:00:00'),
    (103, 2, 3, '2023-11-27 10:00:00', '2023-11-29 09:00:00'),
    (104, 2, 4, '2023-11-28 12:00:00', '2023-11-30 11:00:00'),
    (105, 3, 5, '2023-11-29 08:00:00', '2023-12-01 13:00:00'),
    (106, 4, 6, '2023-11-30 16:00:00', '2023-12-02 10:00:00'),
    (107, 5, 7, '2023-12-01 12:00:00', '2023-12-03 09:00:00'),
    (108, 6, 8, '2023-12-02 14:00:00', '2023-12-04 11:00:00'),
    (109, 7, 9, '2023-12-03 10:00:00', '2023-12-05 08:00:00'),
    (110, 8, 10, '2023-12-04 15:00:00', '2023-12-06 12:00:00');

INSERT INTO Preference (customerId, preference) 
  VALUES 
  (1, 'High floor, away from elevator'),
  (2, 'Close to gym, extra pillows'),
  (3, 'Ocean view, king-sized bed'),
  (4, 'City view, high floor'),
  (5, 'Room service, late checkout'),
  (6, 'Nearby restaurants recommendation'),
  (7, 'Extra toiletries, quiet room'),
  (8, 'Early check-in, late check-out'),
  (9, 'Accessible room, bathroom grab bars'),
  (10, 'Non-smoking room, pet-friendly');




  


