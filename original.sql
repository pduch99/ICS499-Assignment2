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
(1,'Trey Lervick','trey.lervick@gmail.com','651-555-1234','9142 Courtly Road','Woodbury','MN','55125',7,'Attack'),
(2,'Connor Hooley','connor.hooley@yahoo.com','(651) 555-7821','7734 Steeple View Road','Woodbury','MN','55125',22,'Midfield'),
(3,'Big D\'Sosa','big.dsosa+lax@gmail.com','763.555.0199','10475 Ojibway Drive','Woodbury','MN','55129',14,'Defense'),
(4,'MARCUS WEBB','MWEBB@GMAIL.COM','9525550188','8830 Kings Drive','Woodbury','MN','55125',31,'Goalie'),
(5,'Trevor Babtiste Jr.','trevor.babtiste@gmail.com','651-555-0111','7715 Lamplight Drive','Woodbury','MN','55125',9,'Midfield'),
(6,'Dani Rojas','dani.rojas@umn.edu',NULL,'10920 Wooddale Drive','Woodbury','MN','55129',18,'Attack');

INSERT INTO `guardians` (`guardian_id`, `player_id`, `contact_name`, `contact_email`, `contact_phone`, `relationship`) VALUES
(101,1,'Rachel Lervick','rachel.lervick@gmail.com','651-555-4410','mother'),
(102,2,'Sean Hooley','sean.hooley@yahoo.com','(651) 555-7822','father'),
(103,3,'Priya D''Sosa','priya.dsosa@gmail.com','763-555-0200','mother'),
(104,1,'Rachel Lervick','rachel.lervick@gmail.com','651-555-4410','guardian'),
(105,6,'Dani Rojas','dani.rojas@umn.edu','651-555-3377','self');

INSERT INTO `away_trips` VALUES
(9001,1,'Trey Lervick','9142 Courtly Road, Woodbury, MN 55125','2024-04-13'),
(9002,2,'Connor Hooley','7734 Steeple View Road, Woodbury, MN 55125','2024-04-13'),
(9003,4,'MARCUS WEBB','8830 Kings Drive, Woodbury, MN 55125','2024-04-20'),
(9004,1,'Trey Lervick','9142 Courtly Road, Woodbury, MN 55125','2024-05-04');

INSERT INTO `venues` (`venue_id`, `name`, `field_surface`) VALUES
(1,'Bielenberg Sports Center','Turf'),
(2,'National Sports Center','Grass'),
(3,'M Health Fairview Sports Center','Turf');