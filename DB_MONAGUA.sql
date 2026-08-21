-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: monagua_db
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auditoria_auditoria`
--

DROP TABLE IF EXISTS `auditoria_auditoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auditoria_auditoria` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `acciones_realizada` varchar(255) NOT NULL,
  `tabla_afectada` varchar(100) NOT NULL,
  `fecha` date NOT NULL,
  `hora` time(6) NOT NULL,
  `observacion` longtext,
  `valor_anterior` longtext,
  `nuevo_valor` longtext,
  `codigo_usuario_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auditoria_auditoria_codigo_usuario_id_32002ef5_fk_usuarios_` (`codigo_usuario_id`),
  CONSTRAINT `auditoria_auditoria_codigo_usuario_id_32002ef5_fk_usuarios_` FOREIGN KEY (`codigo_usuario_id`) REFERENCES `usuarios_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `catalogo_actividades`
--

DROP TABLE IF EXISTS `catalogo_actividades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `catalogo_actividades` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext NOT NULL,
  `nivel_dificultad` varchar(10) NOT NULL,
  `equipo_requerimiento` longtext NOT NULL,
  `recomendaciones` longtext NOT NULL,
  `estado` tinyint(1) NOT NULL,
  `apto_menores` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `catalogo_categoria`
--

DROP TABLE IF EXISTS `catalogo_categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `catalogo_categoria` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext NOT NULL,
  `estado` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `catalogo_paquete`
--

DROP TABLE IF EXISTS `catalogo_paquete`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `catalogo_paquete` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `imagen` varchar(100) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` longtext NOT NULL,
  `dias_duracion` int unsigned NOT NULL,
  `noches_duracion` int unsigned NOT NULL,
  `punto_encuentro` varchar(200) NOT NULL,
  `hora_encuentro` time(6) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  `categoria_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `catalogo_paquete_categoria_id_7d04e189_fk_catalogo_categoria_id` (`categoria_id`),
  CONSTRAINT `catalogo_paquete_categoria_id_7d04e189_fk_catalogo_categoria_id` FOREIGN KEY (`categoria_id`) REFERENCES `catalogo_categoria` (`id`),
  CONSTRAINT `catalogo_paquete_chk_1` CHECK ((`dias_duracion` >= 0)),
  CONSTRAINT `catalogo_paquete_chk_2` CHECK ((`noches_duracion` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `catalogo_tarifa`
--

DROP TABLE IF EXISTS `catalogo_tarifa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `catalogo_tarifa` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `precio_adulto` int NOT NULL,
  `precio_menor` int NOT NULL,
  `estado` varchar(10) NOT NULL,
  `paquete_id` bigint NOT NULL,
  `temporada_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `catalogo_tarifa_paquete_id_temporada_id_70f49d1f_uniq` (`paquete_id`,`temporada_id`),
  KEY `catalogo_tarifa_temporada_id_2dc7f294_fk_catalogo_temporada_id` (`temporada_id`),
  CONSTRAINT `catalogo_tarifa_paquete_id_cd744ffa_fk_catalogo_paquete_id` FOREIGN KEY (`paquete_id`) REFERENCES `catalogo_paquete` (`id`),
  CONSTRAINT `catalogo_tarifa_temporada_id_2dc7f294_fk_catalogo_temporada_id` FOREIGN KEY (`temporada_id`) REFERENCES `catalogo_temporada` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `catalogo_temporada`
--

DROP TABLE IF EXISTS `catalogo_temporada`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `catalogo_temporada` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `descripcion` longtext NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `estado` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `comunidad_blog`
--

DROP TABLE IF EXISTS `comunidad_blog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comunidad_blog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `titulo` varchar(200) NOT NULL,
  `contenido` longtext NOT NULL,
  `informacion_adicional` longtext NOT NULL,
  `imagen_destacada` varchar(100) DEFAULT NULL,
  `fecha_publicacion` datetime(6) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  `usuario_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `comunidad_blog_usuario_id_0e6de3ee_fk_usuarios_usuario_id` (`usuario_id`),
  CONSTRAINT `comunidad_blog_usuario_id_0e6de3ee_fk_usuarios_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `comunidad_calificacion`
--

DROP TABLE IF EXISTS `comunidad_calificacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comunidad_calificacion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tipo` varchar(20) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `puntaje_estrellas` smallint unsigned NOT NULL,
  `comentario` longtext NOT NULL,
  `visible` tinyint(1) NOT NULL,
  `admin_respuesta` longtext,
  `fecha_calificacion` datetime(6) NOT NULL,
  `reserva_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `comunidad_calificaci_reserva_id_19d4b005_fk_reservas_` (`reserva_id`),
  CONSTRAINT `comunidad_calificaci_reserva_id_19d4b005_fk_reservas_` FOREIGN KEY (`reserva_id`) REFERENCES `reservas_reserva` (`id`),
  CONSTRAINT `comunidad_calificacion_chk_1` CHECK ((`puntaje_estrellas` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `comunidad_pqrs`
--

DROP TABLE IF EXISTS `comunidad_pqrs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comunidad_pqrs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tipo` varchar(15) NOT NULL,
  `asunto` varchar(200) NOT NULL,
  `descripcion` longtext NOT NULL,
  `estado` varchar(15) NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `cliente_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `comunidad_pqrs_cliente_id_a47f8a05_fk_usuarios_cliente_id` (`cliente_id`),
  CONSTRAINT `comunidad_pqrs_cliente_id_a47f8a05_fk_usuarios_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `usuarios_cliente` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  KEY `django_admin_log_user_id_c564eba6_fk_usuarios_usuario_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_usuarios_usuario_id` FOREIGN KEY (`user_id`) REFERENCES `usuarios_usuario` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
-- Table structure for table `factura`
--

DROP TABLE IF EXISTS `factura`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `factura` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fecha_emision` datetime(6) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `valor_subtotal` decimal(12,2) NOT NULL,
  `valor_total` decimal(12,2) NOT NULL,
  `codigo_reserva` bigint NOT NULL,
  `codigo_pago` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo_reserva` (`codigo_reserva`),
  KEY `factura_codigo_pago_9de66332_fk_pago_id` (`codigo_pago`),
  CONSTRAINT `factura_codigo_pago_9de66332_fk_pago_id` FOREIGN KEY (`codigo_pago`) REFERENCES `pago` (`id`),
  CONSTRAINT `factura_codigo_reserva_877122db_fk_reservas_reserva_id` FOREIGN KEY (`codigo_reserva`) REFERENCES `reservas_reserva` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pago`
--

DROP TABLE IF EXISTS `pago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pago` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `referencia` varchar(100) NOT NULL,
  `banco_origen` varchar(100) NOT NULL,
  `monto` decimal(12,2) NOT NULL,
  `imagen_comprobante` varchar(100) NOT NULL,
  `descripcion` longtext NOT NULL,
  `estado_transaccion` varchar(20) NOT NULL,
  `nota_admin` longtext NOT NULL,
  `fecha_pago` datetime(6) NOT NULL,
  `fecha_envio` datetime(6) NOT NULL,
  `fecha_revision` datetime(6) DEFAULT NULL,
  `reserva_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reserva_id` (`reserva_id`),
  CONSTRAINT `pago_reserva_id_251d3ecb_fk_reservas_reserva_id` FOREIGN KEY (`reserva_id`) REFERENCES `reservas_reserva` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `paquete_actividades`
--

DROP TABLE IF EXISTS `paquete_actividades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `paquete_actividades` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `dificultad_nivel` varchar(10) NOT NULL,
  `actividad_id` bigint NOT NULL,
  `paquete_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `paquete_actividades_actividad_id_8875204d_fk_catalogo_` (`actividad_id`),
  KEY `paquete_actividades_paquete_id_539abdb4_fk_catalogo_paquete_id` (`paquete_id`),
  CONSTRAINT `paquete_actividades_actividad_id_8875204d_fk_catalogo_` FOREIGN KEY (`actividad_id`) REFERENCES `catalogo_actividades` (`id`),
  CONSTRAINT `paquete_actividades_paquete_id_539abdb4_fk_catalogo_paquete_id` FOREIGN KEY (`paquete_id`) REFERENCES `catalogo_paquete` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `paquete_promociones`
--

DROP TABLE IF EXISTS `paquete_promociones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `paquete_promociones` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `paquete_id` bigint NOT NULL,
  `promocion_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `paquete_promociones_paquete_id_bdab503e_fk_catalogo_paquete_id` (`paquete_id`),
  KEY `paquete_promociones_promocion_id_5286026c_fk_promocion` (`promocion_id`),
  CONSTRAINT `paquete_promociones_paquete_id_bdab503e_fk_catalogo_paquete_id` FOREIGN KEY (`paquete_id`) REFERENCES `catalogo_paquete` (`id`),
  CONSTRAINT `paquete_promociones_promocion_id_5286026c_fk_promocion` FOREIGN KEY (`promocion_id`) REFERENCES `promociones_promocion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `plan_guia`
--

DROP TABLE IF EXISTS `plan_guia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plan_guia` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `idioma_servicio` varchar(50) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL,
  `fecha_inicio_plan` date NOT NULL,
  `fecha_fin_plan` date NOT NULL,
  `estado` varchar(20) NOT NULL,
  `codigo_guia_turistico` bigint NOT NULL,
  `codigo_paquete` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `plan_guia_codigo_guia_turistic_3198b656_fk_usuarios_` (`codigo_guia_turistico`),
  KEY `plan_guia_codigo_paquete_9caa4824_fk_catalogo_paquete_id` (`codigo_paquete`),
  CONSTRAINT `plan_guia_codigo_guia_turistic_3198b656_fk_usuarios_` FOREIGN KEY (`codigo_guia_turistico`) REFERENCES `usuarios_guiaturistico` (`id`),
  CONSTRAINT `plan_guia_codigo_paquete_9caa4824_fk_catalogo_paquete_id` FOREIGN KEY (`codigo_paquete`) REFERENCES `catalogo_paquete` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `promociones_promocion`
--

DROP TABLE IF EXISTS `promociones_promocion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `promociones_promocion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `descripcion` longtext NOT NULL,
  `descuento` int unsigned NOT NULL,
  `fecha_fin` date NOT NULL,
  `fecha_inicio` date NOT NULL,
  `codigo_promocion` varchar(20) NOT NULL,
  `condiciones` longtext,
  `codigo_cupon` varchar(30) DEFAULT NULL,
  `activa` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo_promocion` (`codigo_promocion`),
  CONSTRAINT `promociones_promocion_chk_1` CHECK ((`descuento` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reservas_cancelacion`
--

DROP TABLE IF EXISTS `reservas_cancelacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reservas_cancelacion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `motivo` longtext NOT NULL,
  `penalidad` int NOT NULL,
  `estado` varchar(20) NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `fecha_reembolso` date DEFAULT NULL,
  `valor_reembolsado` int DEFAULT NULL,
  `imagen_comprobante` varchar(100) DEFAULT NULL,
  `reserva_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reservas_cancelacion_reserva_id_39299ab6_fk_reservas_reserva_id` (`reserva_id`),
  CONSTRAINT `reservas_cancelacion_reserva_id_39299ab6_fk_reservas_reserva_id` FOREIGN KEY (`reserva_id`) REFERENCES `reservas_reserva` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reservas_reserva`
--

DROP TABLE IF EXISTS `reservas_reserva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reservas_reserva` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `numero_adultos` int unsigned NOT NULL,
  `numero_menores` int unsigned NOT NULL,
  `estado` varchar(20) NOT NULL,
  `monto_total` int NOT NULL,
  `fecha_registro` datetime(6) NOT NULL,
  `cliente_id` bigint DEFAULT NULL,
  `paquete_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_cliente_paquete_fecha` (`cliente_id`,`paquete_id`,`fecha`),
  KEY `reservas_reserva_paquete_id_4bc9b1f7_fk_catalogo_paquete_id` (`paquete_id`),
  CONSTRAINT `reservas_reserva_cliente_id_78618bc5_fk_usuarios_cliente_id` FOREIGN KEY (`cliente_id`) REFERENCES `usuarios_cliente` (`id`),
  CONSTRAINT `reservas_reserva_paquete_id_4bc9b1f7_fk_catalogo_paquete_id` FOREIGN KEY (`paquete_id`) REFERENCES `catalogo_paquete` (`id`),
  CONSTRAINT `reservas_reserva_chk_1` CHECK ((`numero_adultos` >= 0)),
  CONSTRAINT `reservas_reserva_chk_2` CHECK ((`numero_menores` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seguimiento`
--

DROP TABLE IF EXISTS `seguimiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seguimiento` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `respuesta` longtext NOT NULL,
  `fecha_respuesta` datetime(6) NOT NULL,
  `pqrs_id` bigint NOT NULL,
  `usuario_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `seguimiento_pqrs_id_d785383d_fk_comunidad_pqrs_id` (`pqrs_id`),
  KEY `seguimiento_usuario_id_f2bdcf3f_fk_usuarios_usuario_id` (`usuario_id`),
  CONSTRAINT `seguimiento_pqrs_id_d785383d_fk_comunidad_pqrs_id` FOREIGN KEY (`pqrs_id`) REFERENCES `comunidad_pqrs` (`id`),
  CONSTRAINT `seguimiento_usuario_id_f2bdcf3f_fk_usuarios_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seguros_poliza`
--

DROP TABLE IF EXISTS `seguros_poliza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seguros_poliza` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre_aseguradora` varchar(100) NOT NULL,
  `descripcion` longtext NOT NULL,
  `precio_diario` decimal(10,2) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `seguros_seguroviaje`
--

DROP TABLE IF EXISTS `seguros_seguroviaje`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seguros_seguroviaje` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `numero_poliza` varchar(50) NOT NULL,
  `fecha_emision` datetime(6) NOT NULL,
  `costo_seguro` decimal(12,2) NOT NULL,
  `poliza_id` bigint NOT NULL,
  `reserva_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_poliza` (`numero_poliza`),
  UNIQUE KEY `reserva_id` (`reserva_id`),
  KEY `seguros_seguroviaje_poliza_id_27277a1c_fk_seguros_poliza_id` (`poliza_id`),
  CONSTRAINT `seguros_seguroviaje_poliza_id_27277a1c_fk_seguros_poliza_id` FOREIGN KEY (`poliza_id`) REFERENCES `seguros_poliza` (`id`),
  CONSTRAINT `seguros_seguroviaje_reserva_id_e628d596_fk_reservas_reserva_id` FOREIGN KEY (`reserva_id`) REFERENCES `reservas_reserva` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `usuarios_cliente`
--

DROP TABLE IF EXISTS `usuarios_cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios_cliente` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `pais` varchar(100) NOT NULL,
  `departamento` varchar(100) NOT NULL,
  `ciudad` varchar(100) NOT NULL,
  `usuario_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `usuarios_cliente_usuario_id_e5bb67c3_fk_usuarios_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `usuarios_guiaturistico`
--

DROP TABLE IF EXISTS `usuarios_guiaturistico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios_guiaturistico` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `numero_tarjeta_profesional` varchar(50) NOT NULL,
  `experiencia_anos` int unsigned NOT NULL,
  `experiencia_fecha` date DEFAULT NULL,
  `descripcion_experiencia` longtext NOT NULL,
  `entidad_salud` varchar(100) DEFAULT NULL,
  `usuario_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `usuarios_guiaturisti_usuario_id_cf65119f_fk_usuarios_` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios_usuario` (`id`),
  CONSTRAINT `usuarios_guiaturistico_chk_1` CHECK ((`experiencia_anos` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `usuarios_usuario`
--

DROP TABLE IF EXISTS `usuarios_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios_usuario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  `rol` varchar(20) NOT NULL,
  `tipo_documento` varchar(20) NOT NULL,
  `numero_documento` varchar(20) NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `residencia` varchar(100) NOT NULL,
  `imagen_perfil` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `numero_documento` (`numero_documento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `usuarios_usuario_groups`
--

DROP TABLE IF EXISTS `usuarios_usuario_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios_usuario_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuarios_usuario_groups_usuario_id_group_id_4ed5b09e_uniq` (`usuario_id`,`group_id`),
  KEY `usuarios_usuario_groups_group_id_e77f6dcf_fk_auth_group_id` (`group_id`),
  CONSTRAINT `usuarios_usuario_gro_usuario_id_7a34077f_fk_usuarios_` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios_usuario` (`id`),
  CONSTRAINT `usuarios_usuario_groups_group_id_e77f6dcf_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `usuarios_usuario_user_permissions`
--

DROP TABLE IF EXISTS `usuarios_usuario_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios_usuario_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuarios_usuario_user_pe_usuario_id_permission_id_217cadcd_uniq` (`usuario_id`,`permission_id`),
  KEY `usuarios_usuario_use_permission_id_4e5c0f2f_fk_auth_perm` (`permission_id`),
  CONSTRAINT `usuarios_usuario_use_permission_id_4e5c0f2f_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `usuarios_usuario_use_usuario_id_60aeea80_fk_usuarios_` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-21  9:00:42
