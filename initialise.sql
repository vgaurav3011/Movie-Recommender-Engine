-- MySQL dump 10.13  Distrib 5.7.24, for Linux (x86_64)
--
-- Host: localhost    Database: db_theatre
-- ------------------------------------------------------
-- Server version	5.7.24-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `booked_tickets`
--

DROP TABLE IF EXISTS `booked_tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `booked_tickets` (
  `ticket_no` int(11) NOT NULL,
  `show_id` int(11) NOT NULL,
  `seat_no` int(11) DEFAULT NULL,
  PRIMARY KEY (`ticket_no`,`show_id`),
  KEY `show_id` (`show_id`),
  CONSTRAINT `booked_tickets_ibfk_1` FOREIGN KEY (`show_id`) REFERENCES `shows` (`show_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booked_tickets`
--

LOCK TABLES `booked_tickets` WRITE;
/*!40000 ALTER TABLE `booked_tickets` DISABLE KEYS */;
/*!40000 ALTER TABLE `booked_tickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `halls`
--

DROP TABLE IF EXISTS `halls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `halls` (
  `hall_id` int(11) NOT NULL,
  `class` varchar(10) NOT NULL,
  `no_of_seats` int(11) DEFAULT NULL,
  PRIMARY KEY (`hall_id`,`class`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `halls`
--

LOCK TABLES `halls` WRITE;
/*!40000 ALTER TABLE `halls` DISABLE KEYS */;
INSERT INTO `halls` VALUES (1,'gold',35),(1,'standard',75),(2,'gold',27),(2,'standard',97),(3,'gold',26),(3,'standard',98);
/*!40000 ALTER TABLE `halls` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`newuser`@`localhost`*/ /*!50003 trigger get_price
after insert on halls
for each row
begin

UPDATE shows s, price_listing p 
SET s.price_id=p.price_id 
WHERE p.price_id IN 
(SELECT price_id 
FROM price_listing p 
WHERE dayname(s.Date)=p.day AND s.type=p.type);

end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `movies`
--

DROP TABLE IF EXISTS `movies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `movies` (
  `movie_id` int(11) NOT NULL,
  `movie_name` varchar(40) DEFAULT NULL,
  `length` int(11) DEFAULT NULL,
  `language` varchar(10) DEFAULT NULL,
  `show_start` date DEFAULT NULL,
  `show_end` date DEFAULT NULL,
  PRIMARY KEY (`movie_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movies`
--

LOCK TABLES `movies` WRITE;
/*!40000 ALTER TABLE `movies` DISABLE KEYS */;
/*!40000 ALTER TABLE `movies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `price_listing`
--

DROP TABLE IF EXISTS `price_listing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `price_listing` (
  `price_id` int(11) NOT NULL,
  `type` varchar(3) DEFAULT NULL,
  `day` varchar(10) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  PRIMARY KEY (`price_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `price_listing`
--

LOCK TABLES `price_listing` WRITE;
/*!40000 ALTER TABLE `price_listing` DISABLE KEYS */;
INSERT INTO `price_listing` VALUES (1,'2D','Monday',210),(2,'3D','Monday',295),(3,'4DX','Monday',380),(4,'2D','Tuesday',210),(5,'3D','Tuesday',295),(6,'4DX','Tuesday',380),(7,'2D','Wednesday',210),(8,'3D','Wednesday',295),(9,'4DX','Wednesday',380),(10,'2D','Thursday',210),(11,'3D','Thursday',295),(12,'4DX','Thursday',380),(13,'2D','Friday',320),(14,'3D','Friday',335),(15,'4DX','Friday',495),(16,'2D','Saturday',320),(17,'3D','Saturday',335),(18,'4DX','Saturday',495),(19,'2D','Sunday',320),(20,'3D','Sunday',335),(21,'4DX','Sunday',495);
/*!40000 ALTER TABLE `price_listing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shows`
--

DROP TABLE IF EXISTS `shows`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shows` (
  `show_id` int(11) NOT NULL,
  `movie_id` int(11) DEFAULT NULL,
  `hall_id` int(11) DEFAULT NULL,
  `type` varchar(3) DEFAULT NULL,
  `time` int(11) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `price_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`show_id`),
  KEY `movie_id` (`movie_id`),
  KEY `hall_id` (`hall_id`),
  CONSTRAINT `shows_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`movie_id`),
  CONSTRAINT `shows_ibfk_2` FOREIGN KEY (`hall_id`) REFERENCES `halls` (`hall_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shows`
--

LOCK TABLES `shows` WRITE;
/*!40000 ALTER TABLE `shows` DISABLE KEYS */;
/*!40000 ALTER TABLE `shows` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `types`
--

DROP TABLE IF EXISTS `types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `types` (
  `movie_id` int(11) NOT NULL,
  `type1` varchar(5) DEFAULT NULL,
  `type2` varchar(5) DEFAULT NULL,
  `type3` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`movie_id`),
  CONSTRAINT `types_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`movie_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `types`
--

LOCK TABLES `types` WRITE;
/*!40000 ALTER TABLE `types` DISABLE KEYS */;
/*!40000 ALTER TABLE `types` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-11-24 23:17:40
