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
(1,'Chase Martinez','michael.guzman@yahoo.com','605-960-3410','26710 Chaney Shoals Suite 431','Harperport','LA','13323',7,'Attack'),
(2,'Maria Rogers','john.fox@hotmail.com','(932) 758-9395','450 Whitney Haven Apt. 641','Harperport','LA','13323',22,'Midfield'),
(3,'Eileen Anderson','cody.sims+lax@hotmail.com','526.372.9561','6411 Roger Valley','Harperport','LA','25775',14,'Defense'),
(4,'DAVID JONES','LHALL@YAHOO.COM','6886296991','94705 Jennifer Island','Harperport','LA','13323',31,'Goalie'),
(5,'Christopher Carr Jr.','margaret.martin@gmail.com','718-951-4346','248 Stephens River','Harperport','LA','13323',9,'Midfield'),
(6,'Russell Cook','anthony.harvey@gmail.com',NULL,'7221 Coleman Lane Apt. 981','Harperport','LA','25775',18,'Attack');

INSERT INTO `guardians` (`guardian_id`, `player_id`, `contact_name`, `contact_email`, `contact_phone`, `relationship`) VALUES
(101,1,'Christina Hunter','juan.jones@hotmail.com','732-556-2022','mother'),
(102,2,'Natalie Miller','paul.gilmore@hotmail.com','(237) 901-1486','father'),
(103,3,'Desiree Martinez','michael.white@gmail.com','824-463-2004','mother'),
(104,1,'Christina Hunter','juan.jones@hotmail.com','732-556-2022','guardian'),
(105,6,'Russell Cook','anthony.harvey@gmail.com','896-723-3412','self');

INSERT INTO `away_trips` VALUES
(9001,1,'Chase Martinez','26710 Chaney Shoals Suite 431, Harperport, LA 13323','2024-04-13'),
(9002,2,'Maria Rogers','450 Whitney Haven Apt. 641, Harperport, LA 13323','2024-04-13'),
(9003,4,'DAVID JONES','94705 Jennifer Island, Harperport, LA 13323','2024-04-20'),
(9004,1,'Chase Martinez','26710 Chaney Shoals Suite 431, Harperport, LA 13323','2024-05-04');

INSERT INTO `venues` (`venue_id`, `name`, `field_surface`) VALUES
(1,'Bielenberg Sports Center','Turf'),
(2,'National Sports Center','Grass'),
(3,'M Health Fairview Sports Center','Turf');