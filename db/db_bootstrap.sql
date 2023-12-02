-- This file is to bootstrap a database for the CS3200 project.

-- Create a new database.  You can change the name later.  You'll
-- need this name in the FLASK API file(s),  the AppSmith
-- data source creation.
create database HotelFranchiseDB;

-- Via the Docker Compose file, a special user called webapp will
-- be created in MySQL. We are going to grant that user
-- all privileges to the new database we just created.
-- TODO: If you changed the name of the database above, you need
-- to change it here too.
create user if not exists 'webapp'@'%';
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
    hourlyPay DECIMAL(4,2) NOT NULL,
    role VARCHAR(20) NOT NULL,
    hotelId INTEGER NOT NULL,
    FOREIGN KEY (hotelId) REFERENCES Hotel (hotelId)
         ON UPDATE cascade ON DELETE restrict
);

CREATE TABLE Shift (
    timeOff BOOLEAN,
    employeeId INTEGER,
    dateTimeEnd DATETIME,
    dateTimeStart DATETIME,
    PRIMARY KEY(employeeId, dateTimeStart),
    FOREIGN KEY (employeeId) REFERENCES Employee (employeeId)
        ON UPDATE cascade ON DELETE restrict
);

CREATE TABLE Supplies (
    minUnits INTEGER DEFAULT 1,
    name VARCHAR(15) PRIMARY KEY NOT NULL,
    unitsInStock INTEGER DEFAULT 0,
    hotelId INTEGER,
    FOREIGN KEY (hotelId) REFERENCES Hotel (hotelId)
         ON UPDATE cascade ON DELETE restrict
);

CREATE TABLE Room (
    roomNum INTEGER AUTO_INCREMENT,
    cleaned BOOL DEFAULT 0,
    occupancy INTEGER NOT NULL ,
    hotelId INTEGER,
    yearlyMaintenance DECIMAL(6, 2),
    roomPrice DECIMAL(6, 2),
    PRIMARY KEY (roomNum, hotelId),
    FOREIGN KEY (hotelId) REFERENCES Hotel (hotelId)
         ON UPDATE cascade ON DELETE restrict
);

CREATE TABLE Customer (
    phoneNumber VARCHAR(15) NOT NULL,
    mostRecentStay DATE DEFAULT NULL,
    customerId INTEGER AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(10),
    lastName VARCHAR(10)
);

CREATE TABLE Booking (
    roomNum INTEGER AUTO_INCREMENT,
    hotelId INTEGER,
    customerId INTEGER,
    occupancyStartDate DATETIME,
    occupancyEndDate DATETIME,
    PRIMARY KEY (roomNum, hotelId, customerId),
    FOREIGN KEY (roomNum) REFERENCES Room (roomNum)
        ON UPDATE cascade,
    FOREIGN KEY (hotelId) REFERENCES Room (hotelId)
        ON UPDATE cascade ON DELETE restrict ,
    FOREIGN KEY (customerId) REFERENCES Customer (customerId)
        ON UPDATE cascade ON DELETE restrict
);

CREATE TABLE Preference (
    customerId INTEGER,
    preference VARCHAR(500) PRIMARY KEY,
    FOREIGN KEY (customerId) REFERENCES Customer (customerId)
        ON UPDATE cascade ON DELETE restrict
);

-- Add sample data.
INSERT INTO Hotel (region)
VALUES
  ('Boston'),
  ('New York'),
  ('LA'),
  ('Seattle'),
  ('SF'),
  ('Chicago'),
  ('Denver'),
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

INSERT INTO Customer (phoneNumber, mostRecentStay, firstName, lastName, customerId)
  VALUES 
  ('752-647-6613', '2023-03-05', 'Cullan', 'Eakens', 1),
  ('812-431-6935', '2023-06-09', 'Roselia', 'Davidy', 2),
  ('292-588-3795', '2023-10-31', 'Lila', 'Torr', 3),
  ('998-283-5874', '2023-04-13', 'Julianna', 'Duinbleton', 4),
  ('778-763-2903', '2023-05-09', 'Ynez', 'Cluley', 5),
  ('929-985-0970', '2023-05-28', 'Prinz', 'Blakeney', 6),
  ('337-925-1049', '2023-04-21', 'Forrest', 'Allanson', 7),
  ('183-155-1932', '2023-04-30', 'Sinclair', 'Dodman', 8),
  ('412-623-0505', '2022-12-12', 'Jaymie', 'France', 9),
  ('574-158-3387', '2023-09-24', 'Vonny', 'Sprigings', 10),
  ('674-978-7635', '2023-04-01', 'Meriel', 'Geerling', 11),
  ('632-260-5135', '2023-01-20', 'Nancy', 'Tomney', 12),
  ('807-685-3922', '2023-01-19', 'Jodi', 'Hamnett', 13),
  ('286-321-9410', '2023-07-26', 'Kerwin', 'Peirce', 14),
  ('400-392-9099', '2023-07-12', 'Alexandros', 'Jonah', 15),
  ('338-213-6236', '2023-10-02', 'Averyl', 'Watmore', 16),
  ('683-485-7109', '2023-02-18', 'Allys', 'Stambridge', 17),
  ('988-171-5458', '2023-04-20', 'Kerry', 'Griswaite', 18),
  ('195-971-2247', '2023-05-10', 'Berny', 'Steiner', 19),
  ('431-720-2054', '2023-08-06', 'Cassandry', 'Lowerson', 20),
  ('864-665-7422', '2023-09-28', 'Remington', 'Vasiljevic', 21),
  ('331-880-5649', '2023-09-02', 'Cosmo', 'Schapiro', 22),
  ('950-596-8889', '2023-03-28', 'Saudra', 'Campes', 23),
  ('254-411-0539', '2023-06-25', 'Nicolea', 'Hindmoor', 24),
  ('214-886-3331', '2023-01-10', 'Tracee', 'Marmion', 25),
  ('686-908-1438', '2023-11-10', 'Sibbie', 'Delahunty', 26),
  ('585-264-1926', '2023-08-02', 'Karleen', 'Farrans', 27),
  ('883-998-8257', '2023-09-08', 'Gabbie', 'Craigg', 28),
  ('292-432-9989', '2023-02-07', 'Mariam', 'Bessom', 29),
  ('193-582-6056', '2023-10-08', 'Kanya', 'Charity', 30),
  ('453-888-2682', '2023-06-30', 'Clio', 'Robottham', 31),
  ('548-729-2818', '2023-02-22', 'Madeline', 'Hele', 32),
  ('525-122-3405', '2023-01-03', 'Aaron', 'Thackston', 33),
  ('372-615-9624', '2023-10-30', 'Vitoria', 'Lucey', 34),
  ('418-251-8438', '2023-10-26', 'Sharla', 'Matteuzzi', 35),
  ('639-881-9965', '2023-04-15', 'Kerwin', 'Perrigo', 36),
  ('643-379-7060', '2023-09-25', 'Cooper', 'Sherrell', 37),
  ('916-339-5133', '2023-07-06', 'Emerson', 'Stubbs', 38),
  ('473-851-1393', '2023-12-01', 'Israel', 'Vigar', 39),
  ('712-504-9341', '2023-08-14', 'Raffaello', 'Leghorn', 40),
  ('632-282-8469', '2023-10-23', 'Neel', 'Reside', 41),
  ('261-495-4924', '2023-06-03', 'Rosamond', 'Jahnig', 42),
  ('326-445-1661', '2023-11-25', 'Andreana', 'Elcum', 43),
  ('425-858-7141', '2023-04-05', 'Judi', 'Jeeves', 44),
  ('231-384-2059', '2023-02-27', 'Emanuele', 'Everleigh', 45),
  ('823-946-5415', '2023-05-02', 'Clea', 'McKennan', 46),
  ('120-424-4325', '2023-05-19', 'Nadiya', 'Posner', 47),
  ('805-405-0300', '2023-09-18', 'Nicoline', 'Rayson', 48),
  ('916-343-3795', '2023-04-02', 'Bambi', 'Leyburn', 49),
  ('592-640-1953', '2022-12-28', 'Rikki', 'Switzer', 50),
  ('493-438-6213', '2023-06-23', 'Boote', 'Abrahmer', 51),
  ('117-769-0782', '2023-07-18', 'Elfrieda', 'Hofner', 52),
  ('782-784-0125', '2023-02-15', 'Gay', 'Gaynesford', 53),
  ('648-784-0980', '2023-11-21', 'Emilee', 'Ferrandez', 54),
  ('880-997-0739', '2023-01-17', 'Erinn', 'Vidler', 55),
  ('451-147-8484', '2023-02-26', 'Conrado', 'Coney', 56),
  ('758-946-0230', '2023-03-11', 'Evin', 'Newbigging', 57),
  ('931-589-3682', '2023-08-30', 'Anthony', 'Messenger', 58),
  ('204-563-2363', '2022-12-29', 'Powell', 'Vedstra', 59),
  ('105-249-3372', '2022-12-11', 'Codie', 'Lyte', 60)
;

Insert into Booking (roomNum, hotelId, customerId, occupancyStartDate, occupancyEndDate)
  VALUES
    ('2022-12-30', '2023-05-18', '25', '32', '54'),
    ('2023-11-04', '2023-07-27', '33', '46', '37'), 
    ('2022-12-05', '2023-10-10', '55', '29', '26'), 
    ('2023-04-03', '2023-07-10', '51', '27', '22'), 
    ('2023-04-17', '2023-05-25', '15', '1', '33'), 
    ('2023-10-13', '2023-10-30', '19', '25', '17'), 
    ('2022-12-20', '2023-08-13', '31', '49', '45'), 
    ('2023-09-29', '2023-01-29', '59', '37', '44'), 
    ('2023-02-03', '2023-08-07', '17', '58', '32'), 
    ('2023-01-26', '2023-05-24', '24', '35', '10'), 
    ('2023-08-08', '2023-09-06', '5', '47', '55'), 
    ('2023-01-03', '2023-02-20', '40', '23', '8'), 
    ('2023-02-14', '2023-06-15', '13', '19', '40'), 
    ('2023-04-27', '2023-05-20', '7', '45', '7'), 
    ('2023-11-27', '2023-09-10', '1', '20', '47'), 
    ('2023-04-26', '2023-09-29', '32', '3', '18'), 
    ('2023-04-17', '2023-01-26', '44', '41', '16'), 
    ('2023-01-04', '2023-11-09', '30', '6', '31'), 
    ('2023-04-23', '2023-09-21', '58', '14', '48'), 
    ('2023-07-09', '2023-04-29', '54', '48', '29'), 
    ('2023-10-12', '2023-08-14', '60', '7', '6'), 
    ('2023-08-31', '2023-02-20', '49', '50', '12'), 
    ('2023-12-01', '2023-02-22', '2', '5', '5'), 
    ('2023-01-03', '2023-08-02', '42', '24', '11'), 
    ('2023-04-01', '2023-08-29', '21', '39', '27'), 
    ('2023-06-21', '2023-08-21', '3', '38', '19'), 
    ('2023-02-04', '2023-05-07', '26', '52', '9'), 
    ('2022-12-03', '2023-03-22', '11', '10', '35'), 
    ('2023-06-29', '2023-08-20', '53', '40', '57'), 
    ('2023-03-16', '2023-06-23', '37', '15', '39'), 
    ('2023-04-10', '2023-05-24', '57', '44', '3'), 
    ('2023-10-28', '2023-05-26', '45', '36', '38'), 
    ('2023-01-24', '2023-08-28', '27', '13', '50'), 
    ('2023-06-08', '2023-07-14', '47', '31', '56'), 
    ('2023-11-06', '2023-10-26', '14', '9', '15'), 
    ('2023-05-11', '2023-01-30', '29', '11', '1'), 
    ('2023-09-30', '2023-04-13', '10', '57', '51'), 
    ('2023-08-08', '2023-11-21', '39', '60', '53'), 
    ('2023-09-22', '2023-06-01', '41', '33', '14');

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
