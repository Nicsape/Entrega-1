-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: gimnasio
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `Id_Cliente` int NOT NULL,
  `Nombre` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Id_Cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (1,'AUTO FRENOS BOULEVARD');
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `distribuidor`
--

DROP TABLE IF EXISTS `distribuidor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `distribuidor` (
  `ID_Distribuidor` int NOT NULL,
  `Nombre` varchar(50) DEFAULT NULL,
  `Apellido` varchar(50) DEFAULT NULL,
  `Telefono` varchar(15) DEFAULT NULL,
  `Categoria` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID_Distribuidor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `distribuidor`
--

LOCK TABLES `distribuidor` WRITE;
/*!40000 ALTER TABLE `distribuidor` DISABLE KEYS */;
INSERT INTO `distribuidor` VALUES (1,'Roberto','Gonzales','3108038760','Alimentos'),(2,'Cesar','Sanchez','3132802339','Maquinas'),(3,'Diana','Perez','3024734869','Suplementos'),(4,'Sebastian','Gil','3132802339','Alimentos');
/*!40000 ALTER TABLE `distribuidor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `factura`
--

DROP TABLE IF EXISTS `factura`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `factura` (
  `N_Factura` int NOT NULL,
  `Pago` decimal(10,2) DEFAULT NULL,
  `FK_idusuario` int DEFAULT NULL,
  PRIMARY KEY (`N_Factura`),
  KEY `FK_idusuario` (`FK_idusuario`),
  CONSTRAINT `factura_ibfk_1` FOREIGN KEY (`FK_idusuario`) REFERENCES `usuario` (`ID_Usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `factura`
--

LOCK TABLES `factura` WRITE;
/*!40000 ALTER TABLE `factura` DISABLE KEYS */;
INSERT INTO `factura` VALUES (101,50.00,NULL),(102,120.00,NULL),(103,200.00,NULL);
/*!40000 ALTER TABLE `factura` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario`
--

DROP TABLE IF EXISTS `inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario` (
  `CodigoInv` int NOT NULL,
  `Producto` varchar(50) DEFAULT NULL,
  `Categoria` varchar(50) DEFAULT NULL,
  `Stock` int DEFAULT NULL,
  `Precio` decimal(10,2) DEFAULT NULL,
  `FK_idusuario` int DEFAULT NULL,
  PRIMARY KEY (`CodigoInv`),
  KEY `FK_idusuario` (`FK_idusuario`),
  CONSTRAINT `inventario_ibfk_1` FOREIGN KEY (`FK_idusuario`) REFERENCES `usuario` (`ID_Usuario`),
  CONSTRAINT `inventario_chk_1` CHECK ((`Stock` between 0 and 25))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario`
--

LOCK TABLES `inventario` WRITE;
/*!40000 ALTER TABLE `inventario` DISABLE KEYS */;
INSERT INTO `inventario` VALUES (1,'Proteina','Suplementos',12,96.00,NULL),(2,'Creatina','Suplementos',6,50.00,NULL),(3,'Guantes','Implementos',17,15.00,NULL);
/*!40000 ALTER TABLE `inventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maquinas`
--

DROP TABLE IF EXISTS `maquinas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maquinas` (
  `CodigoMaq` int NOT NULL,
  `Nombre` varchar(50) DEFAULT NULL,
  `Categoria` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`CodigoMaq`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maquinas`
--

LOCK TABLES `maquinas` WRITE;
/*!40000 ALTER TABLE `maquinas` DISABLE KEYS */;
INSERT INTO `maquinas` VALUES (1,'Press Banca','Pecho'),(2,'Sentadilla Libre','Pierna'),(3,'Jalon en polea','Espalda'),(4,'Curl Predicador','Brazo');
/*!40000 ALTER TABLE `maquinas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `membresia`
--

DROP TABLE IF EXISTS `membresia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `membresia` (
  `ID_Membresia` int NOT NULL,
  `Plan` varchar(50) DEFAULT NULL,
  `Costo` decimal(10,2) DEFAULT NULL,
  `Duracion_meses` int DEFAULT NULL,
  `FK_idusuario` int DEFAULT NULL,
  `FK_idpersonal` int DEFAULT NULL,
  PRIMARY KEY (`ID_Membresia`),
  KEY `FK_idusuario` (`FK_idusuario`),
  KEY `FK_idpersonal` (`FK_idpersonal`),
  CONSTRAINT `membresia_ibfk_1` FOREIGN KEY (`FK_idusuario`) REFERENCES `usuario` (`ID_Usuario`),
  CONSTRAINT `membresia_ibfk_2` FOREIGN KEY (`FK_idpersonal`) REFERENCES `personal` (`ID_Personal`),
  CONSTRAINT `membresia_chk_1` CHECK ((`Duracion_meses` between 1 and 12))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `membresia`
--

LOCK TABLES `membresia` WRITE;
/*!40000 ALTER TABLE `membresia` DISABLE KEYS */;
INSERT INTO `membresia` VALUES (1,'Básico',50.00,3,NULL,NULL),(2,'Premium',120.00,6,NULL,NULL),(3,'Anual',200.00,12,NULL,NULL),(4,'Básico',50.00,3,44,NULL);
/*!40000 ALTER TABLE `membresia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personal`
--

DROP TABLE IF EXISTS `personal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personal` (
  `ID_Personal` int NOT NULL,
  `Nombre` varchar(50) DEFAULT NULL,
  `Apellido` varchar(50) DEFAULT NULL,
  `Rol` varchar(50) DEFAULT NULL,
  `Salario` decimal(10,2) DEFAULT NULL,
  `Fecha_Contratacion` date DEFAULT NULL,
  PRIMARY KEY (`ID_Personal`),
  CONSTRAINT `personal_chk_1` CHECK ((`Fecha_Contratacion` <= _utf8mb4'2025-10-27'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personal`
--

LOCK TABLES `personal` WRITE;
/*!40000 ALTER TABLE `personal` DISABLE KEYS */;
INSERT INTO `personal` VALUES (4,'Diego','Vivas','Entrenador',2500.00,'2022-10-21'),(11,'Ana','Torres','Entrenadora',2500.00,'2023-11-10'),(22,'José','Martínez','Recepcionista',1800.00,'2024-05-20'),(33,'Elena','Vargas','Nutricionista',3000.00,'2025-09-15');
/*!40000 ALTER TABLE `personal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `Codigo` varchar(50) NOT NULL,
  `Descripcion` varchar(50) DEFAULT NULL,
  `Precio` int DEFAULT NULL,
  PRIMARY KEY (`Codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES ('1034AMARILLO','FOCOS DE STOP AMARILLO',7),('40222-18000','TORNILLO DE RUEDA DATSUN 210',2),('4651','SILVINES CAJA DE 12 UNIDADES',50),('7313570013','ADITIVO DE MOTOR 14.5 OZS',40),('731357012','ETER',60),('8-94218-497-0','RELAY PARA ISUZU 5P 12V',25),('90311-180754','RETENEDOR RUEDA DELANTERA TOYOTA',75),('AD-35','BANDAS DENTADAS',2),('AT-111-35','FUSES HACHITA MINIATURA 35 AMP',1);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usa_personal_inventario`
--

DROP TABLE IF EXISTS `usa_personal_inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usa_personal_inventario` (
  `ID_Personal` int NOT NULL,
  `Codigo` int NOT NULL,
  `FK_ID_Personal` int DEFAULT NULL,
  `FK_Codigo` int DEFAULT NULL,
  PRIMARY KEY (`ID_Personal`,`Codigo`),
  KEY `FK_ID_Personal` (`FK_ID_Personal`),
  KEY `FK_Codigo` (`FK_Codigo`),
  CONSTRAINT `usa_personal_inventario_ibfk_1` FOREIGN KEY (`FK_ID_Personal`) REFERENCES `personal` (`ID_Personal`),
  CONSTRAINT `usa_personal_inventario_ibfk_2` FOREIGN KEY (`FK_Codigo`) REFERENCES `inventario` (`CodigoInv`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usa_personal_inventario`
--

LOCK TABLES `usa_personal_inventario` WRITE;
/*!40000 ALTER TABLE `usa_personal_inventario` DISABLE KEYS */;
/*!40000 ALTER TABLE `usa_personal_inventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usa_usuario_maquina`
--

DROP TABLE IF EXISTS `usa_usuario_maquina`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usa_usuario_maquina` (
  `ID_Usuario` int NOT NULL,
  `Codigo` int NOT NULL,
  `FK_ID_Usuario` int DEFAULT NULL,
  `FK_Codigo` int DEFAULT NULL,
  PRIMARY KEY (`ID_Usuario`,`Codigo`),
  KEY `FK_ID_Usuario` (`FK_ID_Usuario`),
  KEY `FK_Codigo` (`FK_Codigo`),
  CONSTRAINT `usa_usuario_maquina_ibfk_1` FOREIGN KEY (`FK_ID_Usuario`) REFERENCES `usuario` (`ID_Usuario`),
  CONSTRAINT `usa_usuario_maquina_ibfk_2` FOREIGN KEY (`FK_Codigo`) REFERENCES `maquinas` (`CodigoMaq`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usa_usuario_maquina`
--

LOCK TABLES `usa_usuario_maquina` WRITE;
/*!40000 ALTER TABLE `usa_usuario_maquina` DISABLE KEYS */;
/*!40000 ALTER TABLE `usa_usuario_maquina` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `ID_Usuario` int NOT NULL,
  `Nombre` varchar(50) DEFAULT NULL,
  `Apellido` varchar(50) DEFAULT NULL,
  `Telefono` varchar(15) DEFAULT NULL,
  `Direccion` varchar(100) DEFAULT NULL,
  `Edad` int DEFAULT NULL,
  `Seguro` varchar(50) DEFAULT NULL,
  `Fecha_Registro` date DEFAULT NULL,
  PRIMARY KEY (`ID_Usuario`),
  CONSTRAINT `usuario_chk_1` CHECK ((`Edad` between 16 and 75))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (11,'Carlos','Ramírez','555-1234','Av. Los Pinos 123',25,'Mapfre','2024-06-15'),(22,'María','González','555-5678','Calle Sol 456',34,'Rimac','2025-01-10'),(33,'Luis','Fernández','555-9012','Jr. Luna 789',45,'Pacífico','2025-08-20'),(44,'Juan','Gutierrez','3184220536','Calle 8 #32-11Sur',20,'Rimac','2025-11-21');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vende`
--

DROP TABLE IF EXISTS `vende`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vende` (
  `ID_Distribuidor` int NOT NULL,
  `Codigo` int NOT NULL,
  `FK_ID_Distribuidor` int DEFAULT NULL,
  `FK_Codigo_Inv` int DEFAULT NULL,
  `FK_Codigo_Maq` int DEFAULT NULL,
  PRIMARY KEY (`ID_Distribuidor`,`Codigo`),
  KEY `FK_Codigo_Inv` (`FK_Codigo_Inv`),
  KEY `FK_Codigo_Maq` (`FK_Codigo_Maq`),
  CONSTRAINT `vende_ibfk_1` FOREIGN KEY (`ID_Distribuidor`) REFERENCES `distribuidor` (`ID_Distribuidor`),
  CONSTRAINT `vende_ibfk_2` FOREIGN KEY (`FK_Codigo_Inv`) REFERENCES `inventario` (`CodigoInv`),
  CONSTRAINT `vende_ibfk_3` FOREIGN KEY (`FK_Codigo_Maq`) REFERENCES `maquinas` (`CodigoMaq`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vende`
--

LOCK TABLES `vende` WRITE;
/*!40000 ALTER TABLE `vende` DISABLE KEYS */;
/*!40000 ALTER TABLE `vende` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendedor`
--

DROP TABLE IF EXISTS `vendedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendedor` (
  `ID_Vendedor` int NOT NULL,
  `Nombre` varchar(50) DEFAULT NULL,
  `Apellido` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID_Vendedor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendedor`
--

LOCK TABLES `vendedor` WRITE;
/*!40000 ALTER TABLE `vendedor` DISABLE KEYS */;
INSERT INTO `vendedor` VALUES (1,'Lenin','Salgado');
/*!40000 ALTER TABLE `vendedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'gimnasio'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-19 23:20:42
