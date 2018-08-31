-- MySQL dump 10.13  Distrib 5.6.35, for Linux (x86_64)
--
-- Host: localhost    Database: dailyfresh
-- ------------------------------------------------------
-- Server version	5.7.17

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group__permission_id_16e179c01bf28a0e_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group__permission_id_16e179c01bf28a0e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permission_group_id_683fb80417c42c00_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `auth__content_type_id_53554996ba8befc0_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can add group',3,'add_group'),(9,'Can change group',3,'change_group'),(10,'Can delete group',3,'delete_group'),(11,'Can view group',3,'view_group'),(12,'Can view permission',2,'view_permission'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add 用户',6,'add_user'),(22,'Can change 用户',6,'change_user'),(23,'Can delete 用户',6,'delete_user'),(24,'Can add 地址',7,'add_address'),(25,'Can change 地址',7,'change_address'),(26,'Can delete 地址',7,'delete_address'),(27,'Can view 地址',7,'view_address'),(28,'Can view 用户',6,'view_user'),(29,'Can add 商品种类',8,'add_goodstype'),(30,'Can change 商品种类',8,'change_goodstype'),(31,'Can delete 商品种类',8,'delete_goodstype'),(32,'Can add 商品SPU',9,'add_goods'),(33,'Can change 商品SPU',9,'change_goods'),(34,'Can delete 商品SPU',9,'delete_goods'),(35,'Can add 商品',10,'add_goodssku'),(36,'Can change 商品',10,'change_goodssku'),(37,'Can delete 商品',10,'delete_goodssku'),(38,'Can add 商品图片',11,'add_goodsimage'),(39,'Can change 商品图片',11,'change_goodsimage'),(40,'Can delete 商品图片',11,'delete_goodsimage'),(41,'Can add 首页轮播商品',12,'add_indexgoodsbanner'),(42,'Can change 首页轮播商品',12,'change_indexgoodsbanner'),(43,'Can delete 首页轮播商品',12,'delete_indexgoodsbanner'),(44,'Can add 主页分类展示商品',13,'add_indextypegoodsbanner'),(45,'Can change 主页分类展示商品',13,'change_indextypegoodsbanner'),(46,'Can delete 主页分类展示商品',13,'delete_indextypegoodsbanner'),(47,'Can add 主页促销活动',14,'add_indexpromotionbanner'),(48,'Can change 主页促销活动',14,'change_indexpromotionbanner'),(49,'Can delete 主页促销活动',14,'delete_indexpromotionbanner'),(50,'Can view 商品SPU',9,'view_goods'),(51,'Can view 商品图片',11,'view_goodsimage'),(52,'Can view 商品',10,'view_goodssku'),(53,'Can view 商品种类',8,'view_goodstype'),(54,'Can view 首页轮播商品',12,'view_indexgoodsbanner'),(55,'Can view 主页促销活动',14,'view_indexpromotionbanner'),(56,'Can view 主页分类展示商品',13,'view_indextypegoodsbanner'),(57,'Can add 订单',15,'add_orderinfo'),(58,'Can change 订单',15,'change_orderinfo'),(59,'Can delete 订单',15,'delete_orderinfo'),(60,'Can add 订单商品',16,'add_ordergoods'),(61,'Can change 订单商品',16,'change_ordergoods'),(62,'Can delete 订单商品',16,'delete_ordergoods'),(63,'Can view 订单商品',16,'view_ordergoods'),(64,'Can view 订单',15,'view_orderinfo'),(65,'Can add Bookmark',17,'add_bookmark'),(66,'Can change Bookmark',17,'change_bookmark'),(67,'Can delete Bookmark',17,'delete_bookmark'),(68,'Can add User Setting',18,'add_usersettings'),(69,'Can change User Setting',18,'change_usersettings'),(70,'Can delete User Setting',18,'delete_usersettings'),(71,'Can add User Widget',19,'add_userwidget'),(72,'Can change User Widget',19,'change_userwidget'),(73,'Can delete User Widget',19,'delete_userwidget'),(74,'Can add log entry',20,'add_log'),(75,'Can change log entry',20,'change_log'),(76,'Can delete log entry',20,'delete_log'),(77,'Can view Bookmark',17,'view_bookmark'),(78,'Can view log entry',20,'view_log'),(79,'Can view User Setting',18,'view_usersettings'),(80,'Can view User Widget',19,'view_userwidget');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `df_address`
--

DROP TABLE IF EXISTS `df_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `df_address` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `receiver` varchar(20) NOT NULL,
  `addr` varchar(256) NOT NULL,
  `zip_code` varchar(6) DEFAULT NULL,
  `phone` varchar(11) NOT NULL,
  `is_default` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `df_address_user_id_12c14098429e5c30_fk_df_user_id` (`user_id`),
  CONSTRAINT `df_address_user_id_12c14098429e5c30_fk_df_user_id` FOREIGN KEY (`user_id`) REFERENCES `df_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `df_address`
--

LOCK TABLES `df_address` WRITE;
/*!40000 ALTER TABLE `df_address` DISABLE KEYS */;
INSERT INTO `df_address` VALUES (44,'2018-08-13 10:52:38.657314','2018-08-24 15:55:44.295628',0,'王刚','北京市东城区北京站东街8号信通大厦A座','120110','15801031556',0,32),(50,'2018-08-13 11:16:00.859872','2018-08-27 17:02:04.922765',0,'英子','北京市大兴区兴华中路110号','102909','13156909231',0,35),(60,'2018-08-22 11:55:21.744580','2018-08-24 15:55:44.479645',0,'李明','天津市河北区梅厂镇朱家庄10号','201110','13211235645',1,32),(61,'2018-08-27 17:02:03.377487','2018-08-27 17:02:05.039631',0,'啊是','阿斯蒂啊','111111','15801031556',1,35);
/*!40000 ALTER TABLE `df_address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `df_goods`
--

DROP TABLE IF EXISTS `df_goods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `df_goods` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(20) NOT NULL,
  `detail` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `df_goods`
--

LOCK TABLES `df_goods` WRITE;
/*!40000 ALTER TABLE `df_goods` DISABLE KEYS */;
INSERT INTO `df_goods` VALUES (2,'2018-08-14 16:06:11.638616','2018-08-17 18:17:53.616017',0,'草莓','<p>很不错的草莓</p>'),(3,'2018-08-14 16:06:22.964306','2018-08-14 16:06:22.964306',0,'葡萄','<p>葡萄</p>'),(4,'2018-08-14 16:06:38.844546','2018-08-14 16:06:38.844546',0,'奇异果','<p>奇异果</p>'),(5,'2018-08-14 16:06:48.596223','2018-08-14 16:06:48.596223',0,'柠檬','<p>柠檬</p>'),(6,'2018-08-14 16:07:05.924300','2018-08-14 16:07:05.924799',0,'大青虾','<p>大青虾</p>'),(7,'2018-08-14 16:07:20.470030','2018-08-14 16:07:20.470030',0,'秋刀鱼','<p>秋刀鱼</p>'),(8,'2018-08-14 16:07:39.108507','2018-08-14 16:07:39.109003',0,'扇贝','<p>扇贝</p>'),(9,'2018-08-14 16:07:49.452229','2018-08-14 16:07:49.452727',0,'基围虾','<p>基围虾</p>'),(10,'2018-08-14 16:07:58.837931','2018-08-14 16:07:58.837931',0,'猪肉','<p>猪肉</p>'),(11,'2018-08-14 16:08:09.526453','2018-08-14 16:08:09.526453',0,'牛肉','<p>牛肉</p>'),(12,'2018-08-14 16:08:21.034469','2018-08-14 16:08:21.034469',0,'羊肉','<p>羊肉</p>'),(13,'2018-08-14 16:08:31.607919','2018-08-14 16:08:31.607919',0,'牛排','<p>牛排</p>'),(14,'2018-08-14 16:08:41.442634','2018-08-14 16:08:41.442634',0,'鸡蛋','<p>鸡蛋</p>'),(15,'2018-08-14 16:08:49.216523','2018-08-14 16:08:49.216523',0,'鸡肉','<p>鸡肉</p>'),(16,'2018-08-14 16:09:01.660231','2018-08-14 16:09:01.660231',0,'鸭蛋','<p>鸭蛋</p>'),(17,'2018-08-14 16:09:11.252012','2018-08-14 16:09:11.252012',0,'鸡腿','<p>鸡腿</p>'),(18,'2018-08-14 16:09:20.217850','2018-08-14 16:09:20.217850',0,'白菜','<p>白菜</p>'),(19,'2018-08-14 16:09:29.291273','2018-08-14 16:09:29.291273',0,'芹菜','<p>芹菜</p>'),(20,'2018-08-14 16:09:38.665690','2018-08-14 16:09:38.665690',0,'香菜','<p>香菜</p>'),(21,'2018-08-14 16:09:50.360775','2018-08-14 16:09:50.360775',0,'冬瓜','<p>冬瓜</p>'),(22,'2018-08-14 16:10:03.814934','2018-08-14 16:10:03.814934',0,'鱼丸','<p>鱼丸</p>'),(23,'2018-08-14 16:10:15.760132','2018-08-14 16:10:15.760132',0,'蟹棒','<p>蟹棒</p>'),(24,'2018-08-14 16:10:23.743551','2018-08-14 16:10:23.743551',0,'虾丸','<p>虾丸</p>'),(25,'2018-08-14 16:10:33.038357','2018-08-14 16:10:33.038843',0,'速冻水饺','<p>速冻水饺</p>'),(26,'2018-08-14 16:10:43.121218','2018-08-14 16:10:43.121218',0,'芒果','<p>芒果</p>'),(27,'2018-08-14 16:10:55.852438','2018-08-14 16:10:55.852438',0,'鹌鹑蛋','<p>鹌鹑蛋</p>'),(28,'2018-08-14 16:11:05.379613','2018-08-14 16:11:05.379613',0,'鹅蛋','<p>鹅蛋</p>'),(29,'2018-08-14 16:11:13.045817','2018-08-14 16:11:13.046312',0,'红辣椒','<p>红辣椒</p>');
/*!40000 ALTER TABLE `df_goods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `df_goods_image`
--

DROP TABLE IF EXISTS `df_goods_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `df_goods_image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `image` varchar(100) NOT NULL,
  `sku_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `df_goods_image_22ad5bca` (`sku_id`),
  CONSTRAINT `df_goods_image_sku_id_debb6c8de6a6b1_fk_df_goods_sku_id` FOREIGN KEY (`sku_id`) REFERENCES `df_goods_sku` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `df_goods_image`
--

LOCK TABLES `df_goods_image` WRITE;
/*!40000 ALTER TABLE `df_goods_image` DISABLE KEYS */;
/*!40000 ALTER TABLE `df_goods_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `df_goods_sku`
--

DROP TABLE IF EXISTS `df_goods_sku`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `df_goods_sku` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(20) NOT NULL,
  `desc` varchar(256) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `unite` varchar(20) NOT NULL,
  `image` varchar(100) NOT NULL,
  `stock` int(11) NOT NULL,
  `sales` int(11) NOT NULL,
  `status` smallint(6) NOT NULL,
  `goods_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `df_goods_sku_goods_id_2e5add9bc94f021c_fk_df_goods_id` (`goods_id`),
  KEY `df_goods_sku_94757cae` (`type_id`),
  CONSTRAINT `df_goods_sku_goods_id_2e5add9bc94f021c_fk_df_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `df_goods` (`id`),
  CONSTRAINT `df_goods_sku_type_id_58a77b6da8bfe771_fk_df_goods_type_id` FOREIGN KEY (`type_id`) REFERENCES `df_goods_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `df_goods_sku`
--

LOCK TABLES `df_goods_sku` WRITE;
/*!40000 ALTER TABLE `df_goods_sku` DISABLE KEYS */;
INSERT INTO `df_goods_sku` VALUES (4,'2018-08-14 16:15:08.452414','2018-08-27 16:08:42.654057',0,'草莓','大兴草莓',10.00,'500g','group1/M00/00/00/wKgTg1tylJ6AbXJOAAEc8FlxEvU9936403',0,4,1,2,2),(5,'2018-08-14 16:15:48.430620','2018-08-27 10:58:08.218301',0,'盒装草莓','大兴奶油草莓',20.00,'盒','group1/M00/00/00/wKgTg1tyj7eAXuKeAAAljHPuXJg9320842',99,1,1,2,2),(6,'2018-08-14 16:16:35.949342','2018-08-27 16:59:38.819315',0,'葡萄','采育葡萄',20.00,'500g','group1/M00/00/00/wKgTg1tyj-eAJYoDAAAjjiYTEkw1894740',88,12,1,3,2),(8,'2018-08-14 16:18:30.021914','2018-08-24 13:57:20.918648',0,'奇异果','海南奇异果',12.33,'500g','group1/M00/00/00/wKgTg1tykFmAGvKBAAAeuLYy0pU2874869',0,1,1,4,2),(9,'2018-08-14 16:19:32.403499','2018-08-14 16:19:32.403499',0,'大青虾','天津大青虾',34.00,'500g','group1/M00/00/00/wKgTg1tykJeAOdCuAAAk0DN4-yE0000584',100,0,1,6,3),(10,'2018-08-14 16:20:10.163913','2018-08-24 15:45:34.001276',0,'秋刀鱼','北海道秋刀鱼',50.00,'500g','group1/M00/00/00/wKgTg1tykL2AQNUUAAAkaP_7_189281285',0,3,0,7,3),(11,'2018-08-14 16:20:55.925352','2018-08-27 16:08:42.141610',0,'扇贝','大连扇贝',56.60,'500g','group1/M00/00/00/wKgTg1tykOuAYU78AAAk8WCqqmI5822209',92,8,1,8,3),(12,'2018-08-14 16:21:34.499616','2018-08-27 11:42:57.505003',0,'基围虾','越南基围虾',100.80,'500g','group1/M00/00/00/wKgTg1tykRGAJ4ULAAA5OS4Kl4c4194242',97,3,1,9,3),(13,'2018-08-14 16:22:18.824946','2018-08-14 16:22:18.824946',0,'猪肉','大兴猪肉',23.00,'500g','group1/M00/00/00/wKgTg1tykT6AAMZ_AAEVpb1YHUE2100329',1,0,1,10,4),(14,'2018-08-14 16:23:00.606886','2018-08-24 20:25:00.135746',0,'牛肉','新疆牛肉',34.99,'500g','group1/M00/00/00/wKgTg1tykWeAdKV_AAEExAU4yXU2934265',0,1,1,11,4),(15,'2018-08-14 16:23:50.390263','2018-08-24 16:50:03.017524',0,'羊肉','山东羊肉',56.88,'500g','group1/M00/00/00/wKgTg1tykZmAfk94AAB6NOQDrpk0380805',0,1,1,12,4),(16,'2018-08-14 16:24:28.301486','2018-08-24 16:50:05.193183',0,'牛排','新鲜牛排',99.80,'500g','group1/M00/00/00/wKgTg1tykb-AXwj3AACwa3rCDPQ9079102',0,1,1,13,4),(17,'2018-08-14 16:25:37.465855','2018-08-24 16:55:33.188797',0,'盒装鸡蛋','散养鸡蛋',23.00,'盒','group1/M00/00/00/wKgTg1tykgSADVvYAADUKbwLSqY5269795',99,1,1,14,5),(18,'2018-08-14 16:27:02.328932','2018-08-24 16:03:59.856463',0,'鸡肉','农家散养鸡',32.00,'500g','group1/M00/00/00/wKgTg1tyklmAT-PdAADUY5hC_sI8187167',21,2,1,15,5),(19,'2018-08-14 16:27:38.818113','2018-08-14 16:27:38.818113',0,'鸭蛋','白洋淀鸭蛋',45.00,'盒','group1/M00/00/00/wKgTg1tykn6ACOrdAAFC_2tSkFo3750771',100,0,1,16,5),(20,'2018-08-14 16:28:17.046940','2018-08-27 11:55:25.491226',0,'鸡腿','笨鸡鸡腿',32.00,'500g','group1/M00/00/00/wKgTg1tykqSAUXZNAAA2_p7G96w7234113',9,3,1,17,5),(21,'2018-08-14 16:28:58.215136','2018-08-27 16:08:41.604043',0,'白菜','山东大白菜',4.50,'500g','group1/M00/00/00/wKgTg1tyks2AAiihAADWHYeKaNI2260987',0,1,1,18,6),(22,'2018-08-14 16:29:32.897896','2018-08-27 12:41:52.769806',0,'芹菜','北京小芹菜',3.50,'500g','group1/M00/00/00/wKgTg1tykvCAQl1EAACIrzuaK643839906',42,1,1,19,6),(23,'2018-08-14 16:30:33.455989','2018-08-14 16:30:33.455989',0,'香菜','房山香菜',8.80,'500g','group1/M00/00/00/wKgTg1tykyyAD4_dAACNpHC0IEY2866287',34,0,1,20,6),(24,'2018-08-14 16:31:10.357459','2018-08-27 12:46:06.132937',0,'冬瓜','天津青皮冬瓜',2.99,'500g','group1/M00/00/00/wKgTg1tyk1GAA32pAAENHrNG1-s0836934',98,1,1,21,6),(25,'2018-08-14 16:32:05.258923','2018-08-14 16:32:05.258923',0,'鱼丸','鱼丸',9.80,'500g','group1/M00/00/00/wKgTg1tyk4iAJCh6AADZQphQJ2o2485386',100,0,1,22,7),(26,'2018-08-14 16:32:35.379819','2018-08-27 16:47:45.280802',0,'蟹棒','蟹棒',9.80,'500g','group1/M00/00/00/wKgTg1tyk6aAU0vqAABxy5vKkgY4240868',99,1,1,23,7),(27,'2018-08-14 16:33:07.069150','2018-08-14 16:33:07.069150',0,'虾丸','蟹棒',9.80,'500g','group1/M00/00/00/wKgTg1tyk8aAAofdAABICav_wjk7230924',100,0,1,24,7),(28,'2018-08-14 16:33:38.083690','2018-08-27 16:47:47.509129',0,'速冻水饺','速冻水饺',12.88,'500g','group1/M00/00/00/wKgTg1tyk-WAQBo1AACMoBJXjDs4193732',98,2,1,25,7),(29,'2018-08-14 16:34:50.513219','2018-08-27 16:59:40.531472',0,'芒果','越南芒果',29.80,'500g','group1/M00/00/00/wKgTg1tylC2AXhH-AAByzTJcTjM9834821',95,5,1,26,2),(30,'2018-08-14 16:35:24.011099','2018-08-24 16:55:31.854201',0,'鹌鹑蛋','速冻水饺',18.88,'500g','group1/M00/00/00/wKgTg1tylE-ACIIqAAGZ6KapWiA1575667',95,5,1,27,5),(31,'2018-08-14 16:35:54.873209','2018-08-14 16:35:54.873209',0,'鹅蛋','鹅蛋',32.00,'500g','group1/M00/00/00/wKgTg1tylG6AWTcHAADg_NUp5b46685959',100,0,1,28,5),(32,'2018-08-14 16:36:27.709669','2018-08-14 16:36:27.710165',0,'红辣椒','红辣椒',2.30,'500g','group1/M00/00/00/wKgTg1tylI6AUT9TAAHXO8pdocY3817309',100,0,1,29,6);
/*!40000 ALTER TABLE `df_goods_sku` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `df_goods_type`
--

DROP TABLE IF EXISTS `df_goods_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `df_goods_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(20) NOT NULL,
  `logo` varchar(20) NOT NULL,
  `image` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `df_goods_type`
--

LOCK TABLES `df_goods_type` WRITE;
/*!40000 ALTER TABLE `df_goods_type` DISABLE KEYS */;
INSERT INTO `df_goods_type` VALUES (2,'2018-08-14 15:46:43.545013','2018-08-14 15:46:43.545510',0,'新鲜水果','fruit','group1/M00/00/00/wKgTg1tyiOaAINkCAABChktC5I44380081'),(3,'2018-08-14 15:47:25.036546','2018-08-14 15:47:25.036546',0,'海鲜水产','seafood','group1/M00/00/00/wKgTg1tyiRCAS3v6AAB6Qt2qz7w2453295'),(4,'2018-08-14 15:47:43.451914','2018-08-14 15:47:43.451914',0,'猪牛羊肉','meet','group1/M00/00/00/wKgTg1tyiSKAcIm_AABP_7aqOEg3444390'),(5,'2018-08-14 15:48:04.081182','2018-08-14 15:48:04.081182',0,'禽类蛋品','egg','group1/M00/00/00/wKgTg1tyiTeAQqLXAABDRDMvQes5423422'),(6,'2018-08-14 15:48:56.816993','2018-08-14 15:48:56.816993',0,'新鲜蔬菜','vegetables','group1/M00/00/00/wKgTg1tyiWyAVuYOAABm8oRZzvE9804224'),(7,'2018-08-14 15:49:19.508000','2018-08-14 15:49:19.508000',0,'速冻食品','ice','group1/M00/00/00/wKgTg1tyiYKAcrZ9AABbZbLmza85039469');
/*!40000 ALTER TABLE `df_goods_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `df_index_banner`
--

DROP TABLE IF EXISTS `df_index_banner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `df_index_banner` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `image` varchar(100) NOT NULL,
  `index` smallint(6) NOT NULL,
  `sku_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `df_index_banner_sku_id_6e9fc21fccb13592_fk_df_goods_sku_id` (`sku_id`),
  CONSTRAINT `df_index_banner_sku_id_6e9fc21fccb13592_fk_df_goods_sku_id` FOREIGN KEY (`sku_id`) REFERENCES `df_goods_sku` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `df_index_banner`
--

LOCK TABLES `df_index_banner` WRITE;
/*!40000 ALTER TABLE `df_index_banner` DISABLE KEYS */;
INSERT INTO `df_index_banner` VALUES (1,'2018-08-14 16:47:39.312432','2018-08-14 16:47:39.312432',0,'group1/M00/00/00/wKgTg1tyly-AG3JPAACpB-LsCdE8706202',0,6),(2,'2018-08-14 16:48:36.521570','2018-08-14 16:48:36.521570',0,'group1/M00/00/00/wKgTg1tyl2eAeN6ZAAC3B-z8J2c5507337',1,29),(3,'2018-08-14 16:48:54.098828','2018-08-14 16:48:54.098828',0,'group1/M00/00/00/wKgTg1tyl3mAXJ5gAAETwXb_pso1844595',2,13),(4,'2018-08-14 16:49:08.628250','2018-08-14 16:49:08.628250',0,'group1/M00/00/00/wKgTg1tyl4eAbbJNAAD0akkXmFo3934665',3,10);
/*!40000 ALTER TABLE `df_index_banner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `df_index_promotion`
--

DROP TABLE IF EXISTS `df_index_promotion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `df_index_promotion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `name` varchar(20) NOT NULL,
  `url` varchar(200) NOT NULL,
  `image` varchar(100) NOT NULL,
  `index` smallint(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `df_index_promotion`
--

LOCK TABLES `df_index_promotion` WRITE;
/*!40000 ALTER TABLE `df_index_promotion` DISABLE KEYS */;
INSERT INTO `df_index_promotion` VALUES (1,'2018-08-14 17:00:19.587677','2018-08-16 15:35:11.930345',0,'吃货暑假趴','http://www.baidu.com','group1/M00/00/00/wKgTg1tymiaAaOjaAAA2pLUeB600430264',3),(2,'2018-08-14 17:00:47.765339','2018-08-14 17:04:14.906052',0,'盛夏尝鲜季','http://www.toutiao.com','group1/M00/00/00/wKgTg1tymkOAIsRPAAA98yvCs1I4019578',1);
/*!40000 ALTER TABLE `df_index_promotion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `df_index_type_goods`
--

DROP TABLE IF EXISTS `df_index_type_goods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `df_index_type_goods` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `display_type` smallint(6) NOT NULL,
  `index` smallint(6) NOT NULL,
  `sku_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `df_index_type_goods_sku_id_e2276ec34291dc8_fk_df_goods_sku_id` (`sku_id`),
  KEY `df_index_type_goods_type_id_67533dddcbf23268_fk_df_goods_type_id` (`type_id`),
  CONSTRAINT `df_index_type_goods_sku_id_e2276ec34291dc8_fk_df_goods_sku_id` FOREIGN KEY (`sku_id`) REFERENCES `df_goods_sku` (`id`),
  CONSTRAINT `df_index_type_goods_type_id_67533dddcbf23268_fk_df_goods_type_id` FOREIGN KEY (`type_id`) REFERENCES `df_goods_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `df_index_type_goods`
--

LOCK TABLES `df_index_type_goods` WRITE;
/*!40000 ALTER TABLE `df_index_type_goods` DISABLE KEYS */;
/*!40000 ALTER TABLE `df_index_type_goods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `df_order_goods`
--

DROP TABLE IF EXISTS `df_order_goods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `df_order_goods` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `count` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `comment` varchar(256) DEFAULT NULL,
  `order_id` varchar(128) NOT NULL,
  `sku_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `df_order_goods_69dfcb07` (`order_id`),
  KEY `df_order_goods_22ad5bca` (`sku_id`),
  CONSTRAINT `df_order_goo_order_id_6667cc4a36aa0b17_fk_df_order_info_order_id` FOREIGN KEY (`order_id`) REFERENCES `df_order_info` (`order_id`),
  CONSTRAINT `df_order_goods_sku_id_5f6eee2492a199a5_fk_df_goods_sku_id` FOREIGN KEY (`sku_id`) REFERENCES `df_goods_sku` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `df_order_goods`
--

LOCK TABLES `df_order_goods` WRITE;
/*!40000 ALTER TABLE `df_order_goods` DISABLE KEYS */;
INSERT INTO `df_order_goods` VALUES (20,'2018-08-24 16:50:03.016160','2018-08-27 15:22:38.906642',0,1,56.88,'还好','2018082416500293227250',15),(21,'2018-08-24 16:50:05.191813','2018-08-27 15:22:39.084351',0,1,99.80,'还好','2018082416500293227250',16),(22,'2018-08-24 16:50:05.452591','2018-08-27 15:22:39.094504',0,1,20.00,'还好','2018082416500293227250',6),(23,'2018-08-24 16:55:31.852859','2018-08-24 16:55:31.852859',0,1,18.88,NULL,'2018082416553144862138',30),(24,'2018-08-24 16:55:33.187447','2018-08-24 16:55:33.187447',0,1,23.00,NULL,'2018082416553144862138',17),(25,'2018-08-24 16:56:27.518046','2018-08-24 16:56:27.518046',0,1,10.00,NULL,'2018082416562709635972',4),(26,'2018-08-24 19:55:55.500554','2018-08-24 19:55:55.500554',0,1,100.80,NULL,'2018082419555582471868',12),(27,'2018-08-24 20:25:00.134327','2018-08-24 20:25:00.134327',0,1,34.99,NULL,'2018082420250057209501',14),(28,'2018-08-25 15:10:39.154213','2018-08-25 15:10:39.154213',0,1,12.88,NULL,'2018082515103976228354',28),(29,'2018-08-27 10:58:08.216903','2018-08-27 10:58:08.216903',0,1,20.00,NULL,'2018082710580851741848',5),(30,'2018-08-27 10:58:09.775819','2018-08-27 10:58:09.775819',0,1,29.80,NULL,'2018082710580851741848',29),(31,'2018-08-27 10:58:10.430353','2018-08-27 10:58:10.430353',0,1,10.00,NULL,'2018082710580851741848',4),(32,'2018-08-27 11:42:57.503573','2018-08-27 11:42:57.504287',0,1,100.80,NULL,'2018082711425754905957',12),(33,'2018-08-27 11:55:25.489819','2018-08-27 15:29:53.188422',0,1,32.00,'都坏了啊','2018082711552559643560',20),(34,'2018-08-27 12:41:52.767708','2018-08-27 15:25:30.583787',0,1,3.50,'as','2018082712415296218498',22),(35,'2018-08-27 12:46:06.130858','2018-08-27 15:19:40.664446',0,1,2.99,'很不好吃','2018082712460514722890',24),(36,'2018-08-27 16:08:39.824861','2018-08-27 16:10:26.995201',0,3,29.80,'很好吃，东西很好的','2018082716083997757108',29),(37,'2018-08-27 16:08:41.602369','2018-08-27 16:10:27.102229',0,1,4.50,'嘎嘣脆甜','2018082716083997757108',21),(38,'2018-08-27 16:08:42.139935','2018-08-27 16:10:27.112801',0,7,56.60,'个大肉多，味道非常鲜美','2018082716083997757108',11),(39,'2018-08-27 16:08:42.652383','2018-08-27 16:10:27.123680',0,1,10.00,'奶油味的，物美价廉','2018082716083997757108',4),(40,'2018-08-27 16:47:45.277945','2018-08-27 16:49:38.688260',0,1,9.80,'不好吃，香精味太浓了','2018082716474522850125',26),(41,'2018-08-27 16:47:47.506987','2018-08-27 16:49:38.800581',0,1,12.88,'快过期了，一点不新鲜','2018082716474522850125',28),(42,'2018-08-27 16:59:38.817155','2018-08-27 17:02:35.147929',0,1,20.00,'真的很不错啊，很甜的，我很喜欢，已经买了很多次了，','2018082716593809168947',6),(43,'2018-08-27 16:59:40.530032','2018-08-27 17:01:46.485525',0,1,29.80,'个头大，汁多，非常甜','2018082716593809168947',29);
/*!40000 ALTER TABLE `df_order_goods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `df_order_info`
--

DROP TABLE IF EXISTS `df_order_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `df_order_info` (
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `order_id` varchar(128) NOT NULL,
  `pay_method` smallint(6) NOT NULL,
  `total_count` int(11) NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `transit_price` decimal(10,2) NOT NULL,
  `order_status` smallint(6) NOT NULL,
  `trade_no` varchar(128) NOT NULL,
  `addr_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`order_id`),
  KEY `df_order_info_90ccbf41` (`addr_id`),
  KEY `df_order_info_e8701ad4` (`user_id`),
  CONSTRAINT `df_order_info_addr_id_5d8bdd924cb4f606_fk_df_address_id` FOREIGN KEY (`addr_id`) REFERENCES `df_address` (`id`),
  CONSTRAINT `df_order_info_user_id_35b90923dea5c691_fk_df_user_id` FOREIGN KEY (`user_id`) REFERENCES `df_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `df_order_info`
--

LOCK TABLES `df_order_info` WRITE;
/*!40000 ALTER TABLE `df_order_info` DISABLE KEYS */;
INSERT INTO `df_order_info` VALUES ('2018-08-24 16:50:02.954719','2018-08-27 15:22:39.101031',0,'2018082416500293227250',3,3,186.68,10.00,5,'2018082721001004440200571453',60,32),('2018-08-24 16:55:31.768858','2018-08-24 16:55:33.441463',0,'2018082416553144862138',3,2,51.88,10.00,1,'',60,32),('2018-08-24 16:56:27.458190','2018-08-27 12:55:40.689644',0,'2018082416562709635972',3,1,20.00,10.00,4,'2018082421001004440500362024',60,32),('2018-08-24 19:55:55.370825','2018-08-24 19:55:57.069962',0,'2018082419555582471868',3,1,110.80,10.00,1,'',60,32),('2018-08-24 20:25:00.062003','2018-08-24 20:25:00.560719',0,'2018082420250057209501',1,1,44.99,10.00,1,'',60,32),('2018-08-25 15:10:39.041304','2018-08-25 15:10:39.632326',0,'2018082515103976228354',3,1,22.88,10.00,1,'',60,32),('2018-08-27 10:58:08.047829','2018-08-27 10:58:10.880294',0,'2018082710580851741848',4,3,69.80,10.00,1,'',60,32),('2018-08-27 11:42:57.386369','2018-08-27 15:39:08.178834',0,'2018082711425754905957',3,1,110.80,10.00,4,'2018082721001004440200571458',60,32),('2018-08-27 11:55:25.337051','2018-08-27 15:29:53.308101',0,'2018082711552559643560',3,1,42.00,10.00,5,'2018082721001004440200571449',60,32),('2018-08-27 12:41:52.621019','2018-08-27 15:25:30.699563',0,'2018082712415296218498',3,1,13.50,10.00,5,'2018082721001004440500362554',60,32),('2018-08-27 12:46:05.961685','2018-08-27 15:19:40.839209',0,'2018082712460514722890',3,1,12.99,10.00,5,'2018082721001004440200571450',60,32),('2018-08-27 16:08:39.357285','2018-08-27 16:10:27.131422',0,'2018082716083997757108',3,12,510.10,10.00,5,'2018082721001004440500362560',44,32),('2018-08-27 16:47:45.104279','2018-08-27 16:49:38.808901',0,'2018082716474522850125',3,2,32.68,10.00,5,'2018082721001004440200571459',60,32),('2018-08-27 16:59:38.647955','2018-08-27 17:01:46.492297',0,'2018082716593809168947',3,2,59.80,10.00,5,'2018082721001004440200571460',50,35);
/*!40000 ALTER TABLE `df_order_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `df_user`
--

DROP TABLE IF EXISTS `df_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `df_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `is_delete` tinyint(1) NOT NULL,
  `gender` varchar(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `df_user`
--

LOCK TABLES `df_user` WRITE;
/*!40000 ALTER TABLE `df_user` DISABLE KEYS */;
INSERT INTO `df_user` VALUES (32,'pbkdf2_sha256$24000$EFnKH8SoLvDj$5r/BAW8pV4mvSb6jabmLLT1omu5z5KfwQ1AcCHelA0g=','2018-08-27 17:03:18.351152',1,'administrator','','','',1,1,'2018-08-10 09:15:08.331222','2018-08-10 09:15:08.360982','2018-08-14 11:39:03.776232',0,'male'),(35,'pbkdf2_sha256$24000$FxqX4CadbGDi$qXmUk1h+5uIUAb0z2YVnaWto5AVybv0/u04T0WGMWDA=','2018-08-27 17:02:46.876157',0,'1059653878@qq.com','','','1059653878@qq.com',0,1,'2018-08-13 11:14:41.607086','2018-08-13 11:14:41.636847','2018-08-13 11:15:03.800607',0,'male'),(42,'pbkdf2_sha256$24000$iIE99PphUKe8$rvHiW2/nY3K6hqBBW31SHf8O8iUaVQw4WrW+QUW9zf8=',NULL,0,'893695711@qq.com','','','893695711@qq.com',0,0,'2018-08-13 13:54:16.393068','2018-08-13 13:54:16.423807','2018-08-13 13:54:16.427775',0,'male'),(43,'pbkdf2_sha256$24000$iqAi0imNvCIM$RgosYyfpLdAKGAzeSKJ2qGVqj+FGgsLnRz9QnPtcCZ8=',NULL,0,'132342232@qq.com','','','132342232@qq.com',0,0,'2018-08-14 14:16:04.843084','2018-08-14 14:16:04.869392','2018-08-14 14:16:04.879301',0,'male'),(44,'pbkdf2_sha256$24000$pQmDD1O3PRXd$45TyqxRpASJymBpoKayfdEiykMlYoTHjKy1heAayB4M=','2018-08-22 13:44:43.731242',0,'wadayu@163.com','','','wadayu@163.com',1,1,'2018-08-15 14:41:00.000000','2018-08-15 14:41:43.042284','2018-08-22 13:44:33.922776',0,'male');
/*!40000 ALTER TABLE `df_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `df_user_groups`
--

DROP TABLE IF EXISTS `df_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `df_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `df_user_groups_group_id_5211a7f230777f01_fk_auth_group_id` (`group_id`),
  CONSTRAINT `df_user_groups_group_id_5211a7f230777f01_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `df_user_groups_user_id_a8c9e37554089dc_fk_df_user_id` FOREIGN KEY (`user_id`) REFERENCES `df_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `df_user_groups`
--

LOCK TABLES `df_user_groups` WRITE;
/*!40000 ALTER TABLE `df_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `df_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `df_user_user_permissions`
--

DROP TABLE IF EXISTS `df_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `df_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `df_user_use_permission_id_1e38e0b8900605f0_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `df_user_use_permission_id_1e38e0b8900605f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `df_user_user_permissions_user_id_42efc92786be0879_fk_df_user_id` FOREIGN KEY (`user_id`) REFERENCES `df_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `df_user_user_permissions`
--

LOCK TABLES `df_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `df_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `df_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `djang_content_type_id_1502418b3d00a2b8_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_6ec93cb77ef11f0b_fk_df_user_id` (`user_id`),
  CONSTRAINT `djang_content_type_id_1502418b3d00a2b8_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_6ec93cb77ef11f0b_fk_df_user_id` FOREIGN KEY (`user_id`) REFERENCES `df_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_758a6f2dea271e51_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(9,'goods','goods'),(11,'goods','goodsimage'),(10,'goods','goodssku'),(8,'goods','goodstype'),(12,'goods','indexgoodsbanner'),(14,'goods','indexpromotionbanner'),(13,'goods','indextypegoodsbanner'),(16,'order','ordergoods'),(15,'order','orderinfo'),(5,'sessions','session'),(7,'user','address'),(6,'user','user'),(17,'xadmin','bookmark'),(20,'xadmin','log'),(18,'xadmin','usersettings'),(19,'xadmin','userwidget');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2018-08-08 09:44:44.578177'),(2,'contenttypes','0002_remove_content_type_name','2018-08-08 09:44:44.674880'),(3,'auth','0001_initial','2018-08-08 09:44:44.980447'),(4,'auth','0002_alter_permission_name_max_length','2018-08-08 09:44:45.047868'),(5,'auth','0003_alter_user_email_max_length','2018-08-08 09:44:45.059772'),(6,'auth','0004_alter_user_username_opts','2018-08-08 09:44:45.073000'),(7,'auth','0005_alter_user_last_login_null','2018-08-08 09:44:45.090198'),(8,'auth','0006_require_contenttypes_0002','2018-08-08 09:44:45.096145'),(9,'user','0001_initial','2018-08-08 09:44:45.539899'),(10,'admin','0001_initial','2018-08-08 09:44:45.696636'),(11,'goods','0001_initial','2018-08-08 09:44:46.383079'),(12,'order','0001_initial','2018-08-08 09:44:46.449873'),(13,'order','0002_auto_20180807_1656','2018-08-08 09:44:46.991762'),(14,'sessions','0001_initial','2018-08-08 09:44:47.049956'),(15,'admin','0002_logentry_remove_auto_add','2018-08-08 10:09:08.714811'),(16,'auth','0007_alter_validators_add_error_messages','2018-08-08 10:09:08.729770'),(17,'user','0002_auto_20180808_1005','2018-08-08 10:09:08.838048'),(18,'xadmin','0001_initial','2018-08-08 10:09:09.344361'),(19,'goods','0002_auto_20180808_1123','2018-08-08 11:23:52.354331'),(20,'order','0003_auto_20180816_1715','2018-08-16 17:16:46.488467'),(21,'order','0004_auto_20180816_1722','2018-08-16 17:23:29.927047'),(22,'order','0005_auto_20180824_0916','2018-08-24 09:17:40.115280');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('lnu01pkx5dof38loqw6l4s7wlp9k9m61','NGJhMzE3ZGQ0ZTYxODdiNTY5NTljOWRjY2IxYTc1YWI3MjBmMWZkMTp7IkxJU1RfUVVFUlkiOltbInVzZXIiLCJhZGRyZXNzIl0sIiJdLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjdjZjA0ZGZjOWJkNTE1ZjBmOWZjODU2NjgzNTQxMmExMjhjNzFlNGYiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-08-23 16:14:00.173607');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `xadmin_bookmark`
--

DROP TABLE IF EXISTS `xadmin_bookmark`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xadmin_bookmark` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL,
  `url_name` varchar(64) NOT NULL,
  `query` varchar(1000) NOT NULL,
  `is_share` tinyint(1) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `xadmin_bookma_content_type_id_60941679_fk_django_content_type_id` (`content_type_id`),
  KEY `xadmin_bookmark_user_id_42d307fc_fk_df_user_id` (`user_id`),
  CONSTRAINT `xadmin_bookma_content_type_id_60941679_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `xadmin_bookmark_user_id_42d307fc_fk_df_user_id` FOREIGN KEY (`user_id`) REFERENCES `df_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `xadmin_bookmark`
--

LOCK TABLES `xadmin_bookmark` WRITE;
/*!40000 ALTER TABLE `xadmin_bookmark` DISABLE KEYS */;
/*!40000 ALTER TABLE `xadmin_bookmark` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `xadmin_log`
--

DROP TABLE IF EXISTS `xadmin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xadmin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `ip_addr` char(39) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` varchar(32) NOT NULL,
  `message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `xadmin_log_content_type_id_2a6cb852_fk_django_content_type_id` (`content_type_id`),
  KEY `xadmin_log_user_id_bb16a176_fk_df_user_id` (`user_id`),
  CONSTRAINT `xadmin_log_content_type_id_2a6cb852_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `xadmin_log_user_id_bb16a176_fk_df_user_id` FOREIGN KEY (`user_id`) REFERENCES `df_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=129 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `xadmin_log`
--

LOCK TABLES `xadmin_log` WRITE;
/*!40000 ALTER TABLE `xadmin_log` DISABLE KEYS */;
INSERT INTO `xadmin_log` VALUES (26,'2018-08-10 17:38:03.279710','127.0.0.1',NULL,'','delete','批量删除 9 个 地址',NULL,32),(27,'2018-08-10 18:18:32.362218','127.0.0.1',NULL,'','delete','批量删除 11 个 地址',NULL,32),(28,'2018-08-10 22:17:46.765185','127.0.0.1',NULL,'','delete','批量删除 8 个 地址',NULL,32),(29,'2018-08-10 22:20:15.474617','127.0.0.1',NULL,'','delete','批量删除 1 个 地址',NULL,32),(30,'2018-08-13 08:52:17.992610','127.0.0.1','33','administrator(北京市东城区建国门街道110号)','change','已修改 receiver，addr，zip_code 和 phone 。',7,32),(31,'2018-08-13 11:14:02.516375','127.0.0.1',NULL,'','delete','批量删除 1 个 用户',NULL,32),(32,'2018-08-13 13:38:24.297633','127.0.0.1',NULL,'','delete','批量删除 2 个 用户',NULL,32),(33,'2018-08-13 13:39:23.847635','127.0.0.1',NULL,'','delete','批量删除 1 个 用户',NULL,32),(34,'2018-08-13 13:45:21.233708','127.0.0.1',NULL,'','delete','批量删除 1 个 用户',NULL,32),(35,'2018-08-13 13:48:16.518483','127.0.0.1',NULL,'','delete','批量删除 1 个 用户',NULL,32),(36,'2018-08-13 13:54:05.033161','127.0.0.1',NULL,'','delete','批量删除 1 个 用户',NULL,32),(37,'2018-08-13 14:48:34.762583','127.0.0.1','1','水果','create','已添加',8,32),(38,'2018-08-13 14:48:56.300916','127.0.0.1','1','fruit','create','已添加',9,32),(39,'2018-08-13 14:51:02.748603','127.0.0.1','3','水果','create','已添加',10,32),(40,'2018-08-14 13:54:41.322469','127.0.0.1','1','水果','change','已修改 image 。',8,32),(41,'2018-08-14 14:04:20.755924','127.0.0.1','3','水果','change','已修改 image 。',10,32),(42,'2018-08-14 15:44:08.042029','127.0.0.1',NULL,'','delete','批量删除 1 个 商品',NULL,32),(43,'2018-08-14 15:44:15.778201','127.0.0.1',NULL,'','delete','批量删除 1 个 商品种类',NULL,32),(44,'2018-08-14 15:46:43.575267','127.0.0.1','2','新鲜水果','create','已添加',8,32),(45,'2018-08-14 15:47:25.066802','127.0.0.1','3','海鲜水产','create','已添加',8,32),(46,'2018-08-14 15:47:43.487627','127.0.0.1','4','猪牛羊肉','create','已添加',8,32),(47,'2018-08-14 15:48:04.109452','127.0.0.1','5','禽类蛋品','create','已添加',8,32),(48,'2018-08-14 15:48:56.861633','127.0.0.1','6','新鲜蔬菜','create','已添加',8,32),(49,'2018-08-14 15:49:19.542232','127.0.0.1','7','速冻食品','create','已添加',8,32),(50,'2018-08-14 16:04:25.968239','127.0.0.1',NULL,'','delete','批量删除 1 个 商品SPU',NULL,32),(51,'2018-08-14 16:06:11.642088','127.0.0.1','2','草莓','create','已添加',9,32),(52,'2018-08-14 16:06:22.967286','127.0.0.1','3','葡萄','create','已添加',9,32),(53,'2018-08-14 16:06:38.846034','127.0.0.1','4','奇异果','create','已添加',9,32),(54,'2018-08-14 16:06:48.598206','127.0.0.1','5','柠檬','create','已添加',9,32),(55,'2018-08-14 16:07:05.926283','127.0.0.1','6','大青虾','create','已添加',9,32),(56,'2018-08-14 16:07:20.473506','127.0.0.1','7','秋刀鱼','create','已添加',9,32),(57,'2018-08-14 16:07:39.111488','127.0.0.1','8','扇贝','create','已添加',9,32),(58,'2018-08-14 16:07:49.454708','127.0.0.1','9','基围虾','create','已添加',9,32),(59,'2018-08-14 16:07:58.839920','127.0.0.1','10','猪肉','create','已添加',9,32),(60,'2018-08-14 16:08:09.528436','127.0.0.1','11','牛肉','create','已添加',9,32),(61,'2018-08-14 16:08:21.035956','127.0.0.1','12','羊肉','create','已添加',9,32),(62,'2018-08-14 16:08:31.610400','127.0.0.1','13','牛排','create','已添加',9,32),(63,'2018-08-14 16:08:41.445115','127.0.0.1','14','鸡蛋','create','已添加',9,32),(64,'2018-08-14 16:08:49.217519','127.0.0.1','15','鸡肉','create','已添加',9,32),(65,'2018-08-14 16:09:01.661720','127.0.0.1','16','鸭蛋','create','已添加',9,32),(66,'2018-08-14 16:09:11.253499','127.0.0.1','17','鸡腿','create','已添加',9,32),(67,'2018-08-14 16:09:20.220818','127.0.0.1','18','白菜','create','已添加',9,32),(68,'2018-08-14 16:09:29.292756','127.0.0.1','19','芹菜','create','已添加',9,32),(69,'2018-08-14 16:09:38.667179','127.0.0.1','20','香菜','create','已添加',9,32),(70,'2018-08-14 16:09:50.362758','127.0.0.1','21','冬瓜','create','已添加',9,32),(71,'2018-08-14 16:10:03.816919','127.0.0.1','22','鱼丸','create','已添加',9,32),(72,'2018-08-14 16:10:15.762608','127.0.0.1','23','蟹棒','create','已添加',9,32),(73,'2018-08-14 16:10:23.744541','127.0.0.1','24','虾丸','create','已添加',9,32),(74,'2018-08-14 16:10:33.040826','127.0.0.1','25','速冻水饺','create','已添加',9,32),(75,'2018-08-14 16:10:43.125186','127.0.0.1','26','芒果','create','已添加',9,32),(76,'2018-08-14 16:10:55.854916','127.0.0.1','27','鹌鹑蛋','create','已添加',9,32),(77,'2018-08-14 16:11:05.381100','127.0.0.1','28','鹅蛋','create','已添加',9,32),(78,'2018-08-14 16:11:13.047800','127.0.0.1','29','红辣椒','create','已添加',9,32),(79,'2018-08-14 16:15:08.482174','127.0.0.1','4','新鲜水果','create','已添加',10,32),(80,'2018-08-14 16:15:48.469308','127.0.0.1','5','新鲜水果','create','已添加',10,32),(81,'2018-08-14 16:16:35.994973','127.0.0.1','6','新鲜水果','create','已添加',10,32),(82,'2018-08-14 16:17:23.759345','127.0.0.1','7','新鲜水果','create','已添加',10,32),(83,'2018-08-14 16:18:30.051177','127.0.0.1','8','新鲜水果','create','已添加',10,32),(84,'2018-08-14 16:19:32.438218','127.0.0.1','9','海鲜水产','create','已添加',10,32),(85,'2018-08-14 16:20:10.191829','127.0.0.1','10','海鲜水产','create','已添加',10,32),(86,'2018-08-14 16:20:55.956104','127.0.0.1','11','海鲜水产','create','已添加',10,32),(87,'2018-08-14 16:21:34.527888','127.0.0.1','12','海鲜水产','create','已添加',10,32),(88,'2018-08-14 16:22:18.860656','127.0.0.1','13','猪牛羊肉','create','已添加',10,32),(89,'2018-08-14 16:23:00.648548','127.0.0.1','14','猪牛羊肉','create','已添加',10,32),(90,'2018-08-14 16:23:50.422006','127.0.0.1','15','猪牛羊肉','create','已添加',10,32),(91,'2018-08-14 16:24:28.335213','127.0.0.1','16','猪牛羊肉','create','已添加',10,32),(92,'2018-08-14 16:25:37.498586','127.0.0.1','17','禽类蛋品','create','已添加',10,32),(93,'2018-08-14 16:27:02.359684','127.0.0.1','18','禽类蛋品','create','已添加',10,32),(94,'2018-08-14 16:27:38.865223','127.0.0.1','19','禽类蛋品','create','已添加',10,32),(95,'2018-08-14 16:28:17.076180','127.0.0.1','20','禽类蛋品','create','已添加',10,32),(96,'2018-08-14 16:28:58.252831','127.0.0.1','21','新鲜蔬菜','create','已添加',10,32),(97,'2018-08-14 16:29:32.929147','127.0.0.1','22','新鲜蔬菜','create','已添加',10,32),(98,'2018-08-14 16:30:33.493189','127.0.0.1','23','新鲜蔬菜','create','已添加',10,32),(99,'2018-08-14 16:31:10.385737','127.0.0.1','24','新鲜蔬菜','create','已添加',10,32),(100,'2018-08-14 16:32:05.286699','127.0.0.1','25','速冻食品','create','已添加',10,32),(101,'2018-08-14 16:32:35.419499','127.0.0.1','26','速冻食品','create','已添加',10,32),(102,'2018-08-14 16:33:07.095440','127.0.0.1','27','速冻食品','create','已添加',10,32),(103,'2018-08-14 16:33:38.127837','127.0.0.1','28','速冻食品','create','已添加',10,32),(104,'2018-08-14 16:34:50.544964','127.0.0.1','29','新鲜水果','create','已添加',10,32),(105,'2018-08-14 16:35:24.048801','127.0.0.1','30','禽类蛋品','create','已添加',10,32),(106,'2018-08-14 16:35:54.910904','127.0.0.1','31','禽类蛋品','create','已添加',10,32),(107,'2018-08-14 16:36:27.745383','127.0.0.1','32','新鲜蔬菜','create','已添加',10,32),(108,'2018-08-14 16:36:43.756704','127.0.0.1','4','新鲜水果','change','已修改 image 。',10,32),(109,'2018-08-14 16:47:40.573265','127.0.0.1','1','葡萄','create','已添加',12,32),(110,'2018-08-14 16:48:36.556787','127.0.0.1','2','芒果','create','已添加',12,32),(111,'2018-08-14 16:48:54.132061','127.0.0.1','3','猪肉','create','已添加',12,32),(112,'2018-08-14 16:49:08.679834','127.0.0.1','4','秋刀鱼','create','已添加',12,32),(113,'2018-08-14 17:00:19.619918','127.0.0.1','1','吃货暑假趴','create','已添加',14,32),(114,'2018-08-14 17:00:47.825849','127.0.0.1','2','盛夏尝鲜季','create','已添加',14,32),(115,'2018-08-14 17:04:14.908036','127.0.0.1','2','盛夏尝鲜季','change','已修改 url 。',14,32),(116,'2018-08-14 17:39:55.130090','127.0.0.1','5','芒果','create','已添加',12,32),(117,'2018-08-14 17:40:38.726013','127.0.0.1',NULL,'','delete','批量删除 1 个 首页轮播商品',NULL,32),(118,'2018-08-15 14:41:28.193681','127.0.0.1',NULL,'','delete','批量删除 1 个 用户',NULL,32),(119,'2018-08-22 13:44:33.999657','127.0.0.1','44','wadayu@163.com','change','已修改 last_login 和 is_staff 。',6,32),(120,'2018-08-22 16:47:41.025972','127.0.0.1',NULL,'','delete','批量删除 1 个 商品',NULL,32),(121,'2018-08-24 10:16:42.696514','127.0.0.1',NULL,'','delete','批量删除 1 个 订单',NULL,32),(122,'2018-08-24 14:09:44.526031','127.0.0.1',NULL,'','delete','批量删除 3 个 订单',NULL,32),(123,'2018-08-24 14:26:01.831757','127.0.0.1',NULL,'','delete','批量删除 1 个 订单商品',NULL,32),(124,'2018-08-24 14:26:06.937045','127.0.0.1',NULL,'','delete','批量删除 1 个 订单',NULL,32),(125,'2018-08-24 16:00:28.056200','127.0.0.1',NULL,'','delete','批量删除 1 个 订单',NULL,32),(126,'2018-08-24 16:01:22.939490','127.0.0.1',NULL,'','delete','批量删除 1 个 订单',NULL,32),(127,'2018-08-24 16:49:37.130720','127.0.0.1',NULL,'','delete','批量删除 3 个 订单',NULL,32),(128,'2018-08-27 17:02:35.290505','127.0.0.1','42','2018082716593809168947','change','已修改 comment 。',16,32);
/*!40000 ALTER TABLE `xadmin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `xadmin_usersettings`
--

DROP TABLE IF EXISTS `xadmin_usersettings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xadmin_usersettings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(256) NOT NULL,
  `value` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `xadmin_usersettings_user_id_edeabe4a_fk_df_user_id` (`user_id`),
  CONSTRAINT `xadmin_usersettings_user_id_edeabe4a_fk_df_user_id` FOREIGN KEY (`user_id`) REFERENCES `df_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `xadmin_usersettings`
--

LOCK TABLES `xadmin_usersettings` WRITE;
/*!40000 ALTER TABLE `xadmin_usersettings` DISABLE KEYS */;
INSERT INTO `xadmin_usersettings` VALUES (6,'dashboard:home:pos','',32),(7,'dashboard:home:pos','',44);
/*!40000 ALTER TABLE `xadmin_usersettings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `xadmin_userwidget`
--

DROP TABLE IF EXISTS `xadmin_userwidget`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xadmin_userwidget` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `page_id` varchar(256) NOT NULL,
  `widget_type` varchar(50) NOT NULL,
  `value` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `xadmin_userwidget_user_id_c159233a_fk_df_user_id` (`user_id`),
  CONSTRAINT `xadmin_userwidget_user_id_c159233a_fk_df_user_id` FOREIGN KEY (`user_id`) REFERENCES `df_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `xadmin_userwidget`
--

LOCK TABLES `xadmin_userwidget` WRITE;
/*!40000 ALTER TABLE `xadmin_userwidget` DISABLE KEYS */;
/*!40000 ALTER TABLE `xadmin_userwidget` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-08-28 11:16:24
