--sample roster, eastside tide lacrosse club

CREATE TABLE `players` (
  `player_id` int NOT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `phone` varchar(30) DEFAULT NULL,
  `address_line1` varchar(150) DEFAULT NULL,
  `city` varchar(60) DEFAULT NULL,
  `state` char(2) DEFAULT NULL,
  `zip` varchar(10) DEFAULT NULL,
  `jersey_number` int DEFAULT NULL,
  `position` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
CREATE TABLE `guardians` (
  `guardian_id` int NOT NULL,
  `player_id` int DEFAULT NULL,
  `contact_name` varchar(100) DEFAULT NULL,
  `contact_email` varchar(120) DEFAULT NULL,
  `contact_phone` varchar(30) DEFAULT NULL,
  `relationship` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`guardian_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
CREATE TABLE `away_trips` (
  `trip_id` int NOT NULL,
  `player_id` int DEFAULT NULL,
  `player_name` varchar(100) DEFAULT NULL,
  `pickup_address` varchar(200) DEFAULT NULL,
  `trip_date` date DEFAULT NULL,
  PRIMARY KEY (`trip_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
CREATE TABLE `venues` (
  `venue_id` int NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `field_surface` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`venue_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
INSERT INTO `players` (`player_id`, `full_name`, `email`, `phone`, `address_line1`, `city`, `state`, `zip`, `jersey_number`, `position`) VALUES
(1,'Ronald Brown','charles.freeman@hotmail.com','746-860-3123','8261 Livingston Branch Apt. 601','Brewerburgh','ID','76884',7,'Attack'),
(2,'Haley Graves','dennis.morgan@yahoo.com','(838) 984-0825','96137 David Greens Suite 407','Brewerburgh','ID','76884',22,'Midfield'),
(3,'David Waters','brian.robles+lax@yahoo.com','677.248.5275','9136 Clark Roads Apt. 802','Brewerburgh','ID','71809',14,'Defense'),
(4,'ANTHONY FISHER','KBEARD@HOTMAIL.COM','8084039012','526 Wesley Land Apt. 220','Brewerburgh','ID','76884',31,'Goalie'),
(5,'Linda Bernard Jr.','sharon.west@gmail.com','859-854-9508','0363 Hahn Shores','Brewerburgh','ID','76884',9,'Midfield'),
(6,'Patrick Osborne','samantha.mckinney@yahoo.com',NULL,'2354 Carter Village','Brewerburgh','ID','71809',18,'Attack');

INSERT INTO `guardians` (`guardian_id`, `player_id`, `contact_name`, `contact_email`, `contact_phone`, `relationship`) VALUES
(101,1,'Keith Clark','meagan.olsen@gmail.com','572-291-9631','mother'),
(102,2,'Jessica Hebert','donald.holloway@gmail.com','(847) 424-6197','father'),
(103,3,'Chloe Rose','mariah.miller@gmail.com','510-205-9007','mother'),
(104,1,'Keith Clark','meagan.olsen@gmail.com','572-291-9631','guardian'),
(105,6,'Patrick Osborne','samantha.mckinney@yahoo.com','627-864-8316','self');

INSERT INTO `away_trips` VALUES
(9001,1,'Ronald Brown','8261 Livingston Branch Apt. 601, Brewerburgh, ID 76884','2024-04-13'),
(9002,2,'Haley Graves','96137 David Greens Suite 407, Brewerburgh, ID 76884','2024-04-13'),
(9003,4,'ANTHONY FISHER','526 Wesley Land Apt. 220, Brewerburgh, ID 76884','2024-04-20'),
(9004,1,'Ronald Brown','8261 Livingston Branch Apt. 601, Brewerburgh, ID 76884','2024-05-04');

INSERT INTO `venues` (`venue_id`, `name`, `field_surface`) VALUES
(1,'Bielenberg Sports Center','Turf'),
(2,'National Sports Center','Grass'),
(3,'M Health Fairview Sports Center','Turf');