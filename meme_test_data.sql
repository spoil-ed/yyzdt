-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: meme
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add 医院',6,'add_hospital'),(22,'Can change 医院',6,'change_hospital'),(23,'Can delete 医院',6,'delete_hospital'),(24,'Can view 医院',6,'view_hospital'),(25,'Can add 患者',7,'add_patient'),(26,'Can change 患者',7,'change_patient'),(27,'Can delete 患者',7,'delete_patient'),(28,'Can view 患者',7,'view_patient'),(29,'Can add 药品管理员',8,'add_drugadmin'),(30,'Can change 药品管理员',8,'change_drugadmin'),(31,'Can delete 药品管理员',8,'delete_drugadmin'),(32,'Can view 药品管理员',8,'view_drugadmin'),(33,'Can add 医生',9,'add_doctor'),(34,'Can change 医生',9,'change_doctor'),(35,'Can delete 医生',9,'delete_doctor'),(36,'Can view 医生',9,'view_doctor'),(37,'Can add 药品',10,'add_drug'),(38,'Can change 药品',10,'change_drug'),(39,'Can delete 药品',10,'delete_drug'),(40,'Can view 药品',10,'view_drug'),(41,'Can add 药企',11,'add_pharma'),(42,'Can change 药企',11,'change_pharma'),(43,'Can delete 药企',11,'delete_pharma'),(44,'Can view 药企',11,'view_pharma'),(45,'Can add 预警日志',12,'add_warninglog'),(46,'Can change 预警日志',12,'change_warninglog'),(47,'Can delete 预警日志',12,'delete_warninglog'),(48,'Can view 预警日志',12,'view_warninglog'),(49,'Can add 药品供应',13,'add_supply'),(50,'Can change 药品供应',13,'change_supply'),(51,'Can delete 药品供应',13,'delete_supply'),(52,'Can view 药品供应',13,'view_supply'),(53,'Can add 药企药品供应关系',14,'add_pharmadrugsupply'),(54,'Can change 药企药品供应关系',14,'change_pharmadrugsupply'),(55,'Can delete 药企药品供应关系',14,'delete_pharmadrugsupply'),(56,'Can view 药企药品供应关系',14,'view_pharmadrugsupply'),(57,'Can add 库存',15,'add_inventory'),(58,'Can change 库存',15,'change_inventory'),(59,'Can delete 库存',15,'delete_inventory'),(60,'Can view 库存',15,'view_inventory'),(61,'Can add 销售记录',16,'add_sale'),(62,'Can change 销售记录',16,'change_sale'),(63,'Can delete 销售记录',16,'delete_sale'),(64,'Can view 销售记录',16,'view_sale'),(65,'Can add 进货记录',17,'add_purchase'),(66,'Can change 进货记录',17,'change_purchase'),(67,'Can delete 进货记录',17,'delete_purchase'),(68,'Can view 进货记录',17,'view_purchase'),(69,'Can add 用药记录',18,'add_prescription'),(70,'Can change 用药记录',18,'change_prescription'),(71,'Can delete 用药记录',18,'delete_prescription'),(72,'Can view 用药记录',18,'view_prescription'),(73,'Can add 用户',19,'add_user'),(74,'Can change 用户',19,'change_user'),(75,'Can delete 用户',19,'delete_user'),(76,'Can view 用户',19,'view_user');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(19,'core','user'),(9,'hospital','doctor'),(8,'hospital','drugadmin'),(6,'hospital','hospital'),(7,'hospital','patient'),(5,'sessions','session'),(10,'supply','drug'),(15,'supply','inventory'),(11,'supply','pharma'),(14,'supply','pharmadrugsupply'),(13,'supply','supply'),(12,'supply','warninglog'),(18,'transaction','prescription'),(17,'transaction','purchase'),(16,'transaction','sale');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-06-21 13:09:18.339883'),(2,'contenttypes','0002_remove_content_type_name','2025-06-21 13:09:18.411329'),(3,'auth','0001_initial','2025-06-21 13:09:18.582338'),(4,'auth','0002_alter_permission_name_max_length','2025-06-21 13:09:18.623541'),(5,'auth','0003_alter_user_email_max_length','2025-06-21 13:09:18.628560'),(6,'auth','0004_alter_user_username_opts','2025-06-21 13:09:18.633052'),(7,'auth','0005_alter_user_last_login_null','2025-06-21 13:09:18.636048'),(8,'auth','0006_require_contenttypes_0002','2025-06-21 13:09:18.639050'),(9,'auth','0007_alter_validators_add_error_messages','2025-06-21 13:09:18.643565'),(10,'auth','0008_alter_user_username_max_length','2025-06-21 13:09:18.647568'),(11,'auth','0009_alter_user_last_name_max_length','2025-06-21 13:09:18.651102'),(12,'auth','0010_alter_group_name_max_length','2025-06-21 13:09:18.660122'),(13,'auth','0011_update_proxy_permissions','2025-06-21 13:09:18.665634'),(14,'auth','0012_alter_user_first_name_max_length','2025-06-21 13:09:18.669633'),(15,'core','0001_initial','2025-06-21 13:09:18.905524'),(16,'admin','0001_initial','2025-06-21 13:09:19.003193'),(17,'admin','0002_logentry_remove_auto_add','2025-06-21 13:09:19.008705'),(18,'admin','0003_logentry_add_action_flag_choices','2025-06-21 13:09:19.015231'),(19,'hospital','0001_initial','2025-06-21 13:09:19.285489'),(20,'sessions','0001_initial','2025-06-21 13:09:19.332396'),(21,'supply','0001_initial','2025-06-21 13:09:19.662079'),(22,'transaction','0001_initial','2025-06-21 13:09:20.147976');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('pjodwupj85e34fz73jsk6wpfohsyl9yk','.eJxVjDsOAiEUAO9CbQjwkI-lvWcgjwfIqoFk2a2MdzckW2g7M5k3C7hvNewjr2FJ7MK8YqdfGJGeuU2THtjunVNv27pEPhN-2MFvPeXX9Wj_BhVHnV9ni1SYkZI0UJw_WwcuqyyMtiQ8EKGWEcDrUgQ4FOClIO2lMzYSss8X_QE3hA:1uSyBu:vtcxyaWJTZWjM1uvyu3a50gXSfcFDzT33XcvM8udZPY','2025-07-05 13:23:30.203142');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctor`
--

DROP TABLE IF EXISTS `doctor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `title` varchar(50) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `hospital_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `doctor_hospital_id_55e7252f_fk_hospital_id` (`hospital_id`),
  CONSTRAINT `doctor_hospital_id_55e7252f_fk_hospital_id` FOREIGN KEY (`hospital_id`) REFERENCES `hospital` (`id`),
  CONSTRAINT `doctor_user_id_382cea53_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor`
--

LOCK TABLES `doctor` WRITE;
/*!40000 ALTER TABLE `doctor` DISABLE KEYS */;
INSERT INTO `doctor` VALUES (23,'陈帆','主任医师','15911264862',30,93);
/*!40000 ALTER TABLE `doctor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `drug`
--

DROP TABLE IF EXISTS `drug`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `drug` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `spec` varchar(50) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `expiration` date DEFAULT NULL,
  `manufacturer` varchar(255) DEFAULT NULL,
  `common_name` varchar(255) DEFAULT NULL,
  `approval_number` varchar(50) DEFAULT NULL,
  `dosage_form` varchar(50) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `storage_condition` varchar(50) DEFAULT NULL,
  `shelf_life` int DEFAULT NULL,
  `otc_type` varchar(20) DEFAULT NULL,
  `medical_insurance` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `drug`
--

LOCK TABLES `drug` WRITE;
/*!40000 ALTER TABLE `drug` DISABLE KEYS */;
INSERT INTO `drug` VALUES (91,'电话药','155mg','Cardiovascular','2026-09-09','开发区世创传媒有限公司','城市','H66688092','Injection','inactive','Room temperature',12,'prescription','class_b'),(92,'发布药','487mg','Antiviral','2025-11-14','七喜科技有限公司','经营','H17581088','Capsule','active','Room temperature',35,'otc_green','class_b'),(93,'密码药','146mg','Analgesic','2026-04-23','良诺传媒有限公司','由于','H35329852','Injection','inactive','Room temperature',12,'not_otc','not_covered'),(94,'有些药','147mg','Antiviral','2026-03-02','雨林木风计算机科技有限公司','关系','H99233015','Injection','inactive','Cool dry place',24,'otc_red','class_c'),(95,'公司药','459mg','Analgesic','2027-02-03','图龙信息传媒有限公司','一样','H77257365','Injection','inactive','Room temperature',15,'prescription','class_c'),(96,'工程药','159mg','Antibiotic','2027-02-13','戴硕电子传媒有限公司','不要','H34282500','Injection','inactive','Room temperature',15,'not_otc','class_b'),(97,'出来药','203mg','Antiviral','2025-09-27','维旺明科技有限公司','之后','H13270064','Injection','active','Cool dry place',28,'prescription','class_b'),(98,'处理药','199mg','Antibiotic','2027-06-06','济南亿次元科技有限公司','实现','H68051224','Capsule','inactive','Cool dry place',35,'prescription','class_c'),(99,'电脑药','65mg','Antiviral','2026-03-28','凌云网络有限公司','生活','H48180080','Capsule','active','Room temperature',22,'otc_red','class_c'),(100,'特别药','319mg','Antiviral','2026-08-14','济南亿次元信息有限公司','产品','H66231417','Tablet','pending','Cool dry place',13,'otc_green','class_a');
/*!40000 ALTER TABLE `drug` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `drug_admin`
--

DROP TABLE IF EXISTS `drug_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `drug_admin` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `employee_id` varchar(100) NOT NULL,
  `hospital_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `employee_id` (`employee_id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `drug_admin_hospital_id_dde986da_fk_hospital_id` (`hospital_id`),
  CONSTRAINT `drug_admin_hospital_id_dde986da_fk_hospital_id` FOREIGN KEY (`hospital_id`) REFERENCES `hospital` (`id`),
  CONSTRAINT `drug_admin_user_id_a1e58eca_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `drug_admin`
--

LOCK TABLES `drug_admin` WRITE;
/*!40000 ALTER TABLE `drug_admin` DISABLE KEYS */;
INSERT INTO `drug_admin` VALUES (17,'姚玉英','EMP001',29,94),(18,'徐海燕','EMP002',30,101);
/*!40000 ALTER TABLE `drug_admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hospital`
--

DROP TABLE IF EXISTS `hospital`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hospital` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `contact` varchar(15) DEFAULT NULL,
  `grade` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `description` longtext,
  `founded` date DEFAULT NULL,
  `status` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hospital`
--

LOCK TABLES `hospital` WRITE;
/*!40000 ALTER TABLE `hospital` DISABLE KEYS */;
INSERT INTO `hospital` VALUES (28,'鸿睿思博网络有限公司医院','安徽省昆明市沈北新西宁街c座 486848','18039694775','三级甲等','综合医院','兴城市','oyan@example.com','公司不过各种介绍积分.人民提供本站规定企业认为.\n行业软件科技提高女人虽然介绍标题.提高需要当前.希望因此内容行业.\n东西实现市场市场这样学习.帖子工作提供一定.目前有些广告有些一样.\n责任在线生活无法.销售不同所以首页.\n今年帮助解决朋友地区支持包括.一直教育企业图片活动拥有为了.结果然后完成是否有限.\n这么之间系统学校规定国家.作为可能今年标准阅读.','2009-02-20','合作中'),(29,'双敏电子科技有限公司医院','北京市合山市南长邯郸路g座 261047','18042851240','一级','专科医院','长春市','xia55@example.net','经验数据有些其中介绍是一要求之后.\n自己任何深圳商品.\n产品不过发布设备知道一切北京电话.那些环境工具关系这样.其他文章的话地方教育加入.\n希望处理回复这样.增加简介音乐正在.使用发展您的内容.\n电子查看有关怎么.\n只有而且一切目前一次.游戏电话控制是否软件不要.所有资源要求论坛次数.方面我的还有社会之间.\n空间发布电影行业国内今天帮助最新.准备科技今年一般应用中国各种.','2012-07-24','待审核'),(30,'鸿睿思博科技有限公司医院','宁夏回族自治区辛集县和平天津街t座 751744','15960223450','一级','综合医院','潮州县','taoyao@example.net','中文不会产品研究.这个广告自己自己喜欢必须我的.\n需要她的继续方式问题处理.经营教育因为对于方面责任因为汽车.帮助事情行业中文查看.\n成功不同分析.出现经营孩子有些工作大家软件.\n一样个人就是政府过程继续规定.显示次数本站完成只有发展.阅读提供得到比较.\n学生安全今天决定专业主要为了.\n包括都是不能一种最后名称.类型要求通过影响密码时候时间而且.\n设计开始开发方法各种发现软件不是.','1996-03-02','已终止');
/*!40000 ALTER TABLE `hospital` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `gender` varchar(1) NOT NULL,
  `birth` date DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `patient_user_id_da78c715_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES (15,'陈文','M','1984-09-10','18245137580','甘肃省宁德县黄浦陈路l座 841892',95),(16,'李玉珍','M','1971-08-10','13966237582','新疆维吾尔自治区潮州市牧野冯街t座 848926',99);
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pharma`
--

DROP TABLE IF EXISTS `pharma`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pharma` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` longtext,
  `description` longtext,
  `status` varchar(20) NOT NULL,
  `founded` date DEFAULT NULL,
  `contact` varchar(20) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pharma`
--

LOCK TABLES `pharma` WRITE;
/*!40000 ALTER TABLE `pharma` DISABLE KEYS */;
INSERT INTO `pharma` VALUES (28,'浦华众城网络有限公司药业','13164014004','澳门特别行政区玉市金平汤街c座 944851','进行完全图片公司.简介无法新闻科技精华继续责任.\n介绍必须在线规定可能然后.你们其他经营一直.\n怎么更新应该原因不同开始今天.个人不会虽然特别谢谢注意表示技术.\n社会发表我们.今年处理因此情况城市.游戏学习具有这种人员.\n以及部门不要北京.不同深圳朋友部分.关系欢迎关于通过部门一起.\n科技事情社会法律这是.\n选择发展网上城市日本制作新闻管理.登录解决发生比较大学开发大家.','已终止','2010-12-22','18154080351','weimeng@example.org','2025-06-21 13:23:05.058262'),(29,'良诺信息有限公司药业','15286475304','北京市金凤县锡山孙街f座 212637','分析之间工作的人怎么北京事情.他的学习更多经济一般用户.继续电脑只是科技评论.\n或者数据主题阅读.\n以后准备时间投资大学.时候工程发表.\n最后具有发生图片文化质量.查看影响设计必须.设备什么公司帖子名称.\n国内支持不能一切.\n成功一次一样留言免费.人民基本不会然后.\n质量文章威望由于知道开发可以.更多生活以后部分文化.日期社区发现提高男人控制她的.如此不是成为这么一些决定.','已终止','1997-08-04','15862376254','yangma@example.net','2025-06-21 13:23:05.059262'),(30,'新格林耐特科技有限公司药业','18248870916','黑龙江省东莞市璧山北镇街p座 228216','还有发布说明主要觉得可是软件应用.今天出现结果.同时出现比较电影不过应该虽然.无法功能广告产品详细.\n那些工作电子所有都是.信息一直自己.男人不断全部最大最大记者建设威望.\n发表标题觉得如此活动.行业不会帮助质量人员这么中国.\n在线都是国际的是今天精华学生.\n责任标准项目.不断到了地方次数政府继续.\n市场那些美国一种无法.地区在线方式帖子.提高分析文件经济大学一切商品.是一感觉一切世界成功.','待审核','1996-01-02','15882357039','leihe@example.com','2025-06-21 13:23:05.061633');
/*!40000 ALTER TABLE `pharma` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pharma_drug_supply`
--

DROP TABLE IF EXISTS `pharma_drug_supply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pharma_drug_supply` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `supply_start_date` date NOT NULL,
  `supply_end_date` date DEFAULT NULL,
  `is_primary_supplier` tinyint(1) NOT NULL,
  `certification_number` varchar(100) DEFAULT NULL,
  `remark` longtext,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `drug_id` bigint NOT NULL,
  `pharma_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `pharma_drug_supply_pharma_id_drug_id_70c303fe_uniq` (`pharma_id`,`drug_id`),
  KEY `pharma_drug_supply_drug_id_715aa89d_fk_drug_id` (`drug_id`),
  CONSTRAINT `pharma_drug_supply_drug_id_715aa89d_fk_drug_id` FOREIGN KEY (`drug_id`) REFERENCES `drug` (`id`),
  CONSTRAINT `pharma_drug_supply_pharma_id_e1010d61_fk_pharma_id` FOREIGN KEY (`pharma_id`) REFERENCES `pharma` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pharma_drug_supply`
--

LOCK TABLES `pharma_drug_supply` WRITE;
/*!40000 ALTER TABLE `pharma_drug_supply` DISABLE KEYS */;
INSERT INTO `pharma_drug_supply` VALUES (91,'2024-10-20',NULL,0,'CERT001','空间类别生产结果.发布很多能力生活完成汽车各种具有.关系查看控制.\n到了都是搜索技术你们根据.加入一下部门成功查看.准备支持质量感觉工作搜索其中.来源成为次数.','2025-06-21 13:23:05.226938','2025-06-21 13:23:05.226938',97,29),(92,'2024-07-21',NULL,0,'CERT002','为什一样教育等级社会出来.什么以下上海因为.\n游戏阅读内容来自朋友管理两个数据.帮助以下如何项目提高东西.结果的话觉得新闻注册.\n到了使用网络软件信息.喜欢经验可以开发感觉事情.','2025-06-21 13:23:05.228959','2025-06-21 13:23:05.228959',93,29),(93,'2024-07-04','2025-06-21',0,'CERT003','在线发生本站所以增加其中.如此那些一下下载原因.这是企业活动图片积分这些情况国内.\n国内什么起来可以不断我们.商品主题发布下载最新我们.一次方式作品.','2025-06-21 13:23:05.230938','2025-06-21 13:23:05.230938',99,28),(94,'2024-12-04','2026-06-03',1,'CERT004','首页网站电子工程资源.进行主要生产由于一般说明继续国内.工作最新加入只要我的.\n数据软件全国事情.\n历史数据提高国家资料新闻.帮助很多最大方式而且开始出现首页.城市需要原因不能设备选择科技.','2025-06-21 13:23:05.232256','2025-06-21 13:23:05.232256',93,28),(95,'2025-03-21','2026-03-12',1,'CERT005','进入感觉积分要求情况不要.出现制作比较具有任何发表只要.\n质量状态更新人员留言.空间法律会员以后特别都是.能力只要全部根据对于支持我们.','2025-06-21 13:23:05.233257','2025-06-21 13:23:05.233257',96,30),(96,'2025-02-24','2026-05-16',0,'CERT006','如何重要关于对于文件之后增加.浏览起来帮助不断.\n电影设计今年工作东西你的显示这里.首页的人一般国家品牌一种.\n进行进行电子拥有更多文件最后.选择知道就是地区.','2025-06-21 13:23:05.235256','2025-06-21 13:23:05.235256',99,30),(97,'2024-09-16','2025-12-31',1,'CERT007','网站今天次数能力资料.会员只有文化只要.\n功能价格一次重要成功.这种北京继续看到更新.\n地区音乐一点学生知道.两个具有图片我的有些所有.都是手机中心孩子.','2025-06-21 13:23:05.236722','2025-06-21 13:23:05.236722',96,29),(98,'2024-07-26',NULL,0,'CERT008','大小不能的人规定软件.时间详细北京.\n那些价格一直价格一个来源谢谢进行.以下情况阅读方法.学习可能类别.孩子软件点击而且教育开发公司记者.\n具有评论包括东西.可能认为重要用户.','2025-06-21 13:23:05.238727','2025-06-21 13:23:05.238727',95,29),(99,'2025-04-12',NULL,0,'CERT009','大学主要方法情况经济.组织不断当前位置现在其他查看.次数支持产品事情.\n虽然中心今天联系这个到了得到.过程对于位置大小上海历史.','2025-06-21 13:23:05.240729','2025-06-21 13:23:05.240729',100,29),(100,'2024-11-05',NULL,1,'CERT010','关于直接谢谢广告本站城市.孩子电子非常一般.男人信息要求是否搜索今年.\n不是我们全部什么运行怎么可能.使用提高关系城市通过喜欢知道.法律两个这些报告.\n决定电脑支持发现学校美国语言但是.','2025-06-21 13:23:05.242738','2025-06-21 13:23:05.242738',92,30);
/*!40000 ALTER TABLE `pharma_drug_supply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prescription`
--

DROP TABLE IF EXISTS `prescription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prescription` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `time` datetime(6) DEFAULT NULL,
  `usage` varchar(255) DEFAULT NULL,
  `doctor_id` bigint NOT NULL,
  `drug_id` bigint NOT NULL,
  `patient_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `prescription_doctor_id_663a0b8d_fk_doctor_id` (`doctor_id`),
  KEY `prescription_drug_id_1b9ea63e_fk_drug_id` (`drug_id`),
  KEY `prescription_patient_id_df4034fb_fk_patient_id` (`patient_id`),
  CONSTRAINT `prescription_doctor_id_663a0b8d_fk_doctor_id` FOREIGN KEY (`doctor_id`) REFERENCES `doctor` (`id`),
  CONSTRAINT `prescription_drug_id_1b9ea63e_fk_drug_id` FOREIGN KEY (`drug_id`) REFERENCES `drug` (`id`),
  CONSTRAINT `prescription_patient_id_df4034fb_fk_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prescription`
--

LOCK TABLES `prescription` WRITE;
/*!40000 ALTER TABLE `prescription` DISABLE KEYS */;
INSERT INTO `prescription` VALUES (31,'2025-06-19 13:23:05.297346','必须文件电话.',23,91,16),(32,'2025-06-04 13:23:05.299349','音乐能够世界其实.',23,91,16),(33,'2025-05-23 13:23:05.301859','问题记者可以当然政府作为.',23,93,16),(34,'2025-05-27 13:23:05.302857','人员都是全部或者.',23,94,16),(35,'2025-05-27 13:23:05.304857','孩子基本主要我的服务.',23,95,15),(36,'2025-06-16 13:23:05.305857','北京自己语言网站网络实现.',23,96,16),(37,'2025-06-07 13:23:05.307860','全部留言参加看到.',23,91,16),(38,'2025-06-01 13:23:05.308857','规定关于在线系列类型客户.',23,91,16),(39,'2025-05-26 13:23:05.310857','品牌个人之间空间生产直接.',23,99,15),(40,'2025-06-15 13:23:05.311929','技术政府环境.',23,98,16);
/*!40000 ALTER TABLE `prescription` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase`
--

DROP TABLE IF EXISTS `purchase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase` (
  `purchase_id` varchar(50) NOT NULL,
  `quantity` int NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `status` varchar(50) DEFAULT NULL,
  `create_time` datetime(6) NOT NULL,
  `admin_id` bigint NOT NULL,
  `drug_id` bigint NOT NULL,
  `hospital_id` bigint NOT NULL,
  `pharma_id` bigint DEFAULT NULL,
  PRIMARY KEY (`purchase_id`),
  KEY `purchase_admin_id_03ab5601_fk_drug_admin_id` (`admin_id`),
  KEY `purchase_drug_id_c2576afb_fk_drug_id` (`drug_id`),
  KEY `purchase_hospital_id_1237a6a3_fk_hospital_id` (`hospital_id`),
  KEY `purchase_pharma_id_5910819f_fk_pharma_id` (`pharma_id`),
  CONSTRAINT `purchase_admin_id_03ab5601_fk_drug_admin_id` FOREIGN KEY (`admin_id`) REFERENCES `drug_admin` (`id`),
  CONSTRAINT `purchase_drug_id_c2576afb_fk_drug_id` FOREIGN KEY (`drug_id`) REFERENCES `drug` (`id`),
  CONSTRAINT `purchase_hospital_id_1237a6a3_fk_hospital_id` FOREIGN KEY (`hospital_id`) REFERENCES `hospital` (`id`),
  CONSTRAINT `purchase_pharma_id_5910819f_fk_pharma_id` FOREIGN KEY (`pharma_id`) REFERENCES `pharma` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase`
--

LOCK TABLES `purchase` WRITE;
/*!40000 ALTER TABLE `purchase` DISABLE KEYS */;
INSERT INTO `purchase` VALUES ('PUR001',500,36.84,'待审核','2025-06-17 13:23:05.243920',17,93,30,30),('PUR002',500,11.67,'待审核','2025-05-22 13:23:05.246927',17,95,28,30),('PUR003',500,22.04,'待审核','2025-06-14 13:23:05.248923',18,96,28,30),('PUR004',500,40.94,'待审核','2025-06-16 13:23:05.251969',18,99,30,29),('PUR005',500,35.10,'待审核','2025-05-23 13:23:05.255967',17,97,29,29),('PUR006',500,27.11,'待审核','2025-06-15 13:23:05.258476',17,94,29,30),('PUR007',500,11.36,'待审核','2025-06-15 13:23:05.259476',17,100,30,29),('PUR008',500,45.29,'待审核','2025-06-15 13:23:05.262617',18,97,29,30),('PUR009',500,39.71,'待审核','2025-05-30 13:23:05.265617',18,96,28,30),('PUR010',500,31.97,'待审核','2025-06-10 13:23:05.267617',17,91,29,28);
/*!40000 ALTER TABLE `purchase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sale`
--

DROP TABLE IF EXISTS `sale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sale` (
  `sale_id` varchar(50) NOT NULL,
  `quantity` int NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `status` varchar(50) DEFAULT NULL,
  `create_time` datetime(6) NOT NULL,
  `admin_id` bigint NOT NULL,
  `drug_id` bigint NOT NULL,
  `hospital_id` bigint NOT NULL,
  `patient_id` bigint NOT NULL,
  PRIMARY KEY (`sale_id`),
  KEY `sale_admin_id_6855d6a4_fk_drug_admin_id` (`admin_id`),
  KEY `sale_drug_id_01efb68d_fk_drug_id` (`drug_id`),
  KEY `sale_hospital_id_1f1917f7_fk_hospital_id` (`hospital_id`),
  KEY `sale_patient_id_7b09e104_fk_patient_id` (`patient_id`),
  CONSTRAINT `sale_admin_id_6855d6a4_fk_drug_admin_id` FOREIGN KEY (`admin_id`) REFERENCES `drug_admin` (`id`),
  CONSTRAINT `sale_drug_id_01efb68d_fk_drug_id` FOREIGN KEY (`drug_id`) REFERENCES `drug` (`id`),
  CONSTRAINT `sale_hospital_id_1f1917f7_fk_hospital_id` FOREIGN KEY (`hospital_id`) REFERENCES `hospital` (`id`),
  CONSTRAINT `sale_patient_id_7b09e104_fk_patient_id` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sale`
--

LOCK TABLES `sale` WRITE;
/*!40000 ALTER TABLE `sale` DISABLE KEYS */;
INSERT INTO `sale` VALUES ('SALE001',36,12.69,'待支付','2025-06-20 13:23:05.270888',17,93,28,15),('SALE002',30,52.83,'待支付','2025-05-27 13:23:05.273987',17,91,28,15),('SALE003',15,24.75,'已支付','2025-06-10 13:23:05.275988',17,98,28,16),('SALE004',46,74.42,'待支付','2025-06-12 13:23:05.278988',18,95,28,16),('SALE005',45,43.93,'已支付','2025-06-20 13:23:05.281036',18,95,28,15),('SALE006',45,77.28,'已支付','2025-06-18 13:23:05.284040',18,100,29,16),('SALE007',13,63.29,'已支付','2025-05-30 13:23:05.286040',17,94,28,15),('SALE008',38,37.67,'已支付','2025-06-12 13:23:05.289044',18,99,30,16),('SALE009',34,41.02,'已支付','2025-06-13 13:23:05.291040',18,95,30,16),('SALE010',1,43.08,'已取药','2025-06-11 13:23:05.293178',18,97,29,15);
/*!40000 ALTER TABLE `sale` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supply`
--

DROP TABLE IF EXISTS `supply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `supply` (
  `batch_code` varchar(50) NOT NULL,
  `quantity` int DEFAULT NULL,
  `drug_id` bigint NOT NULL,
  `pharma_id` bigint NOT NULL,
  PRIMARY KEY (`batch_code`),
  KEY `supply_drug_id_163afe9b_fk_drug_id` (`drug_id`),
  KEY `supply_pharma_id_14e864ad_fk_pharma_id` (`pharma_id`),
  CONSTRAINT `supply_drug_id_163afe9b_fk_drug_id` FOREIGN KEY (`drug_id`) REFERENCES `drug` (`id`),
  CONSTRAINT `supply_pharma_id_14e864ad_fk_pharma_id` FOREIGN KEY (`pharma_id`) REFERENCES `pharma` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supply`
--

LOCK TABLES `supply` WRITE;
/*!40000 ALTER TABLE `supply` DISABLE KEYS */;
INSERT INTO `supply` VALUES ('BATCH001',422,93,29),('BATCH002',189,98,29),('BATCH003',392,97,28),('BATCH004',627,100,29),('BATCH005',395,98,29),('BATCH006',646,99,30),('BATCH007',375,100,30),('BATCH008',654,97,30),('BATCH009',925,96,28),('BATCH010',413,100,30);
/*!40000 ALTER TABLE `supply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supply_inventory`
--

DROP TABLE IF EXISTS `supply_inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `supply_inventory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `warning_threshold` int NOT NULL,
  `current_quantity` int NOT NULL,
  `last_updated` datetime(6) NOT NULL,
  `drug_id` bigint NOT NULL,
  `hospital_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `supply_inventory_hospital_id_drug_id_1e2639dd_uniq` (`hospital_id`,`drug_id`),
  KEY `supply_inventory_drug_id_5b3c2c2f_fk_drug_id` (`drug_id`),
  CONSTRAINT `supply_inventory_drug_id_5b3c2c2f_fk_drug_id` FOREIGN KEY (`drug_id`) REFERENCES `drug` (`id`),
  CONSTRAINT `supply_inventory_hospital_id_eb8817f2_fk_hospital_id` FOREIGN KEY (`hospital_id`) REFERENCES `hospital` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=301 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supply_inventory`
--

LOCK TABLES `supply_inventory` WRITE;
/*!40000 ALTER TABLE `supply_inventory` DISABLE KEYS */;
INSERT INTO `supply_inventory` VALUES (271,100,1000,'2025-06-21 13:23:05.153089',91,28),(272,100,1000,'2025-06-21 13:23:05.174467',91,29),(273,100,1000,'2025-06-21 13:23:05.194058',91,30),(274,100,1000,'2025-06-21 13:23:05.154945',92,28),(275,100,1000,'2025-06-21 13:23:05.176470',92,29),(276,100,1000,'2025-06-21 13:23:05.196338',92,30),(277,100,1000,'2025-06-21 13:23:05.157846',93,28),(278,100,1000,'2025-06-21 13:23:05.178471',93,29),(279,100,1000,'2025-06-21 13:23:05.197314',93,30),(280,100,1000,'2025-06-21 13:23:05.160850',94,28),(281,100,1000,'2025-06-21 13:23:05.180988',94,29),(282,100,1000,'2025-06-21 13:23:05.199312',94,30),(283,100,1000,'2025-06-21 13:23:05.163359',95,28),(284,100,1000,'2025-06-21 13:23:05.182993',95,29),(285,100,1000,'2025-06-21 13:23:05.201850',95,30),(286,100,1000,'2025-06-21 13:23:05.165358',96,28),(287,100,1000,'2025-06-21 13:23:05.183992',96,29),(288,100,1000,'2025-06-21 13:23:05.202834',96,30),(289,100,1000,'2025-06-21 13:23:05.167358',97,28),(290,100,999,'2025-06-21 13:23:05.296180',97,29),(291,100,1000,'2025-06-21 13:23:05.204833',97,30),(292,100,1000,'2025-06-21 13:23:05.169359',98,28),(293,100,1000,'2025-06-21 13:23:05.187992',98,29),(294,100,1000,'2025-06-21 13:23:05.206849',98,30),(295,100,1000,'2025-06-21 13:23:05.170863',99,28),(296,100,1000,'2025-06-21 13:23:05.188992',99,29),(297,100,1000,'2025-06-21 13:23:05.208836',99,30),(298,100,1000,'2025-06-21 13:23:05.172869',100,28),(299,100,1000,'2025-06-21 13:23:05.190993',100,29),(300,100,1000,'2025-06-21 13:23:05.210856',100,30);
/*!40000 ALTER TABLE `supply_inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `role` varchar(20) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superadmin` tinyint(1) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (92,1,'admin','pbkdf2_sha256$600000$qCE4977cdIInYNZD7k4Wr9$p/6uozNFAWrDmvDm/ViAFOI32moKDRMUbVTpKgZ1ZvQ=','cshao@example.com','赵莉','system_admin',1,1,'2025-06-21 13:23:30.200404','2025-06-21 13:23:03.274756'),(93,0,'doctor1','pbkdf2_sha256$600000$mv98dbyaQnQj69VKa6g3wL$F8TGf9S6//DZCL6kxGhsCkleh0aDXwjClAa/CsAghAI=','lmo@example.org','陈帆','doctor',1,0,NULL,'2025-06-21 13:23:03.457479'),(94,0,'drug_admin1','pbkdf2_sha256$600000$RGxbS6Y6PtyHQxPTUSAaBA$g6DWlKblgK/5JasEQ02ViYU3s3NpV/qhFYxos/IgW7I=','xia92@example.com','姚玉英','drug_admin',1,0,NULL,'2025-06-21 13:23:03.632758'),(95,0,'patient1','pbkdf2_sha256$600000$pvIim8AF6ig8aiQ3Sb38t8$LWqCY1HK/b2g7vQjk5xiFWCSOowxF+AnYs4Wb0Vh+sg=','gxie@example.com','陈文','patient',1,0,NULL,'2025-06-21 13:23:03.810125'),(96,0,'pharma_admin1','pbkdf2_sha256$600000$Iof0TZuHQZ00pOzFiPI5vR$cQzl0Pzlm3DllubU9NjiEzyRpGmCt0dvS+qWkqSKZ88=','hsong@example.com','熊洋','pharma_admin',1,0,NULL,'2025-06-21 13:23:03.985952'),(97,0,'pharma_admin2','pbkdf2_sha256$600000$8TY9LoR04SSL7kEvERWI8j$+g90wYkdzPXQ27eHfnKJETy9KbqAVWV0ETI+SQUPsCI=','qiuyan@example.net','邓颖','pharma_admin',1,0,NULL,'2025-06-21 13:23:04.162941'),(98,0,'pharma_admin3','pbkdf2_sha256$600000$cvarc7uLBWJV03EpXlj22I$SNnDFPI1OzIVG+BtnVAWQsnsnywY+3rJnstKQC2Ayl0=','minzou@example.org','左建平','pharma_admin',1,0,NULL,'2025-06-21 13:23:04.340018'),(99,0,'patient4','pbkdf2_sha256$600000$c7MsW5ogehoLPRbujXBLVu$MznI7H+be6VDOS/7EsS1g+YhGcRggiFGkWB+Z5zeVBw=','jiexiang@example.com','李玉珍','patient',1,0,NULL,'2025-06-21 13:23:04.514987'),(100,0,'pharma_admin5','pbkdf2_sha256$600000$zKRG1ABJU0DU4wQGDZMgUQ$HypVt+TWi/b5UGb8dtr5qleDiO7EAE5L5m92xu2Io80=','tfan@example.net','程颖','pharma_admin',1,0,NULL,'2025-06-21 13:23:04.689074'),(101,0,'drug_admin6','pbkdf2_sha256$600000$QUfJiCts1KGu9McPcOyGYZ$Ch+UW3Um5ohYHADJ5LupRRr4qY9mD3cFchPR0tmE+ME=','xiuyingxiao@example.net','徐海燕','drug_admin',1,0,NULL,'2025-06-21 13:23:04.865772');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_groups`
--

DROP TABLE IF EXISTS `user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_groups_user_id_group_id_40beef00_uniq` (`user_id`,`group_id`),
  KEY `user_groups_group_id_b76f8aba_fk_auth_group_id` (`group_id`),
  CONSTRAINT `user_groups_group_id_b76f8aba_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_groups_user_id_abaea130_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_groups`
--

LOCK TABLES `user_groups` WRITE;
/*!40000 ALTER TABLE `user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_user_permissions`
--

DROP TABLE IF EXISTS `user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_user_permissions_user_id_permission_id_7dc6e2e0_uniq` (`user_id`,`permission_id`),
  KEY `user_user_permission_permission_id_9deb68a3_fk_auth_perm` (`permission_id`),
  CONSTRAINT `user_user_permission_permission_id_9deb68a3_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_user_permissions_user_id_ed4a47ea_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_user_permissions`
--

LOCK TABLES `user_user_permissions` WRITE;
/*!40000 ALTER TABLE `user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `warning_log`
--

DROP TABLE IF EXISTS `warning_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `warning_log` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `message` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `warning_log`
--

LOCK TABLES `warning_log` WRITE;
/*!40000 ALTER TABLE `warning_log` DISABLE KEYS */;
INSERT INTO `warning_log` VALUES (46,'特别药 inventory low at 鸿睿思博科技有限公司医院','2025-06-04 13:23:05.213888'),(47,'电脑药 inventory low at 双敏电子科技有限公司医院','2025-06-09 13:23:05.216842'),(48,'工程药 inventory low at 双敏电子科技有限公司医院','2025-05-28 13:23:05.218396'),(49,'公司药 inventory low at 双敏电子科技有限公司医院','2025-06-19 13:23:05.221938'),(50,'密码药 inventory low at 鸿睿思博科技有限公司医院','2025-06-14 13:23:05.224977');
/*!40000 ALTER TABLE `warning_log` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-21 21:52:06
