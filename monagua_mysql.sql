-- =============================================================================
-- Script de Base de Datos generado para MySQL Workbench
-- Proyecto: Monagua (MNG_WEB)
-- Modo: BUSINESS (25 tablas)
-- Fecha de generación: 2026-08-17 20:00:57
-- =============================================================================

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema `monagua_db`
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `monagua_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `monagua_db`;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`auditoria_auditoria`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `auditoria_auditoria`;
CREATE TABLE IF NOT EXISTS `auditoria_auditoria` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `acciones_realizada` VARCHAR(255) NOT NULL,
  `tabla_afectada` VARCHAR(100) NOT NULL,
  `fecha` DATE NOT NULL,
  `hora` TIME NOT NULL,
  `observacion` TEXT NULL,
  `valor_anterior` TEXT NULL,
  `nuevo_valor` TEXT NULL,
  `codigo_usuario_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_auditoria_auditoria_codigo_usuario_id`
    FOREIGN KEY (`codigo_usuario_id`)
    REFERENCES `usuarios_usuario` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`catalogo_actividades`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catalogo_actividades`;
CREATE TABLE IF NOT EXISTS `catalogo_actividades` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  `descripcion` LONGTEXT NOT NULL,
  `nivel_dificultad` VARCHAR(10) NOT NULL,
  `equipo_requerimiento` TEXT NOT NULL,
  `recomendaciones` TEXT NOT NULL,
  `estado` TINYINT(1) NOT NULL,
  `apto_menores` TINYINT(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`catalogo_categoria`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catalogo_categoria`;
CREATE TABLE IF NOT EXISTS `catalogo_categoria` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  `descripcion` LONGTEXT NOT NULL,
  `estado` TINYINT(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`catalogo_paquete`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catalogo_paquete`;
CREATE TABLE IF NOT EXISTS `catalogo_paquete` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `imagen` VARCHAR(100) NOT NULL,
  `nombre` VARCHAR(100) NOT NULL,
  `descripcion` LONGTEXT NOT NULL,
  `dias_duracion` INT UNSIGNED NOT NULL,
  `noches_duracion` INT UNSIGNED NOT NULL,
  `punto_encuentro` VARCHAR(200) NOT NULL,
  `hora_encuentro` TIME NOT NULL,
  `estado` TINYINT(1) NOT NULL,
  `categoria_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_catalogo_paquete_categoria_id`
    FOREIGN KEY (`categoria_id`)
    REFERENCES `catalogo_categoria` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`catalogo_tarifa`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catalogo_tarifa`;
CREATE TABLE IF NOT EXISTS `catalogo_tarifa` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `precio_adulto` INT NOT NULL,
  `precio_menor` INT NOT NULL,
  `estado` VARCHAR(10) NOT NULL,
  `paquete_id` BIGINT NOT NULL,
  `temporada_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `catalogo_tarifa_paquete_id_temporada_id_70f49d1f_uniq` (`paquete_id`, `temporada_id` ASC),
  CONSTRAINT `fk_catalogo_tarifa_temporada_id`
    FOREIGN KEY (`temporada_id`)
    REFERENCES `catalogo_temporada` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_catalogo_tarifa_paquete_id`
    FOREIGN KEY (`paquete_id`)
    REFERENCES `catalogo_paquete` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`catalogo_temporada`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `catalogo_temporada`;
CREATE TABLE IF NOT EXISTS `catalogo_temporada` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(50) NOT NULL,
  `descripcion` LONGTEXT NOT NULL,
  `fecha_inicio` DATE NOT NULL,
  `fecha_fin` DATE NOT NULL,
  `estado` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`comunidad_blog`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `comunidad_blog`;
CREATE TABLE IF NOT EXISTS `comunidad_blog` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `titulo` VARCHAR(200) NOT NULL,
  `contenido` LONGTEXT NOT NULL,
  `informacion_adicional` TEXT NOT NULL,
  `imagen_destacada` VARCHAR(100) NULL,
  `fecha_publicacion` DATETIME NOT NULL,
  `estado` TINYINT(1) NOT NULL,
  `usuario_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_comunidad_blog_usuario_id`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `usuarios_usuario` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`comunidad_calificacion`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `comunidad_calificacion`;
CREATE TABLE IF NOT EXISTS `comunidad_calificacion` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `puntaje_estrellas` SMALLINT UNSIGNED NOT NULL,
  `comentario` TEXT NOT NULL,
  `fecha_calificacion` DATETIME NOT NULL,
  `reserva_id` BIGINT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_comunidad_calificacion_reserva_id`
    FOREIGN KEY (`reserva_id`)
    REFERENCES `reservas_reserva` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`comunidad_comentario`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `comunidad_comentario`;
CREATE TABLE IF NOT EXISTS `comunidad_comentario` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `tipo` VARCHAR(20) NOT NULL,
  `titulo` VARCHAR(255) NOT NULL,
  `mensaje` TEXT NOT NULL,
  `valoracion` SMALLINT UNSIGNED NOT NULL,
  `visible` TINYINT(1) NOT NULL,
  `admin_respuesta` TEXT NULL,
  `fecha_creacion` DATETIME NOT NULL,
  `paquete_id` BIGINT NULL,
  `usuario_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_comunidad_comentario_usuario_id`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `usuarios_usuario` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_comunidad_comentario_paquete_id`
    FOREIGN KEY (`paquete_id`)
    REFERENCES `catalogo_paquete` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`comunidad_pqrs`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `comunidad_pqrs`;
CREATE TABLE IF NOT EXISTS `comunidad_pqrs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `tipo` VARCHAR(15) NOT NULL,
  `asunto` VARCHAR(200) NOT NULL,
  `descripcion` LONGTEXT NOT NULL,
  `estado` VARCHAR(15) NOT NULL,
  `fecha` DATETIME NOT NULL,
  `cliente_id` BIGINT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_comunidad_pqrs_cliente_id`
    FOREIGN KEY (`cliente_id`)
    REFERENCES `usuarios_cliente` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`factura`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `factura`;
CREATE TABLE IF NOT EXISTS `factura` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `fecha_emision` DATETIME NOT NULL,
  `estado` VARCHAR(20) NOT NULL,
  `valor_subtotal` DECIMAL(12, 2) NOT NULL,
  `valor_total` DECIMAL(12, 2) NOT NULL,
  `codigo_pago` BIGINT NULL,
  `codigo_reserva` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uq_factura_codigo_reserva` (`codigo_reserva` ASC),
  CONSTRAINT `fk_factura_codigo_reserva`
    FOREIGN KEY (`codigo_reserva`)
    REFERENCES `reservas_reserva` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_factura_codigo_pago`
    FOREIGN KEY (`codigo_pago`)
    REFERENCES `pago` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`pago`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `pago`;
CREATE TABLE IF NOT EXISTS `pago` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `referencia` VARCHAR(100) NOT NULL,
  `banco_origen` VARCHAR(100) NOT NULL,
  `monto` DECIMAL(12, 2) NOT NULL,
  `imagen_comprobante` VARCHAR(100) NOT NULL,
  `descripcion` LONGTEXT NOT NULL,
  `estado_transaccion` VARCHAR(20) NOT NULL,
  `nota_admin` TEXT NOT NULL,
  `fecha_pago` DATETIME NOT NULL,
  `fecha_envio` DATETIME NOT NULL,
  `fecha_revision` DATETIME NULL,
  `usuario_id` BIGINT NOT NULL,
  `reserva_id` BIGINT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uq_pago_reserva_id` (`reserva_id` ASC),
  CONSTRAINT `fk_pago_reserva_id`
    FOREIGN KEY (`reserva_id`)
    REFERENCES `reservas_reserva` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_pago_usuario_id`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `usuarios_usuario` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`paquete_actividades`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `paquete_actividades`;
CREATE TABLE IF NOT EXISTS `paquete_actividades` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `dificultad_nivel` VARCHAR(10) NOT NULL,
  `actividad_id` BIGINT NOT NULL,
  `paquete_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_paquete_actividades_paquete_id`
    FOREIGN KEY (`paquete_id`)
    REFERENCES `catalogo_paquete` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_paquete_actividades_actividad_id`
    FOREIGN KEY (`actividad_id`)
    REFERENCES `catalogo_actividades` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`paquete_promociones`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `paquete_promociones`;
CREATE TABLE IF NOT EXISTS `paquete_promociones` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `paquete_id` BIGINT NOT NULL,
  `promocion_id` BIGINT NOT NULL,
  `tarifa_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_paquete_promociones_tarifa_id`
    FOREIGN KEY (`tarifa_id`)
    REFERENCES `catalogo_tarifa` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_paquete_promociones_promocion_id`
    FOREIGN KEY (`promocion_id`)
    REFERENCES `promociones_promocion` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_paquete_promociones_paquete_id`
    FOREIGN KEY (`paquete_id`)
    REFERENCES `catalogo_paquete` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`plan_guia`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `plan_guia`;
CREATE TABLE IF NOT EXISTS `plan_guia` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `idioma_servicio` VARCHAR(50) NOT NULL,
  `fecha_creacion` DATETIME NOT NULL,
  `fecha_inicio_plan` DATE NOT NULL,
  `fecha_fin_plan` DATE NOT NULL,
  `estado` VARCHAR(20) NOT NULL,
  `codigo_guia_turistico` BIGINT NOT NULL,
  `codigo_paquete` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_plan_guia_codigo_paquete`
    FOREIGN KEY (`codigo_paquete`)
    REFERENCES `catalogo_paquete` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_plan_guia_codigo_guia_turistico`
    FOREIGN KEY (`codigo_guia_turistico`)
    REFERENCES `usuarios_guiaturistico` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`promociones_banner`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promociones_banner`;
CREATE TABLE IF NOT EXISTS `promociones_banner` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `imagen` VARCHAR(100) NOT NULL,
  `titulo` VARCHAR(150) NOT NULL,
  `enlace` VARCHAR(200) NULL,
  `activo` TINYINT(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`promociones_promocion`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `promociones_promocion`;
CREATE TABLE IF NOT EXISTS `promociones_promocion` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(150) NOT NULL,
  `descripcion` LONGTEXT NOT NULL,
  `descuento` INT UNSIGNED NOT NULL,
  `fecha_fin` DATE NOT NULL,
  `fecha_inicio` DATE NOT NULL,
  `codigo_promocion` VARCHAR(20) NOT NULL,
  `condiciones` TEXT NULL,
  `codigo_cupon` VARCHAR(30) NULL,
  `activa` TINYINT(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uq_promociones_promocion_codigo_promocion` (`codigo_promocion` ASC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`reservas_cancelacion`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reservas_cancelacion`;
CREATE TABLE IF NOT EXISTS `reservas_cancelacion` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `motivo` TEXT NOT NULL,
  `penalidad` INT NOT NULL,
  `estado` VARCHAR(20) NOT NULL,
  `fecha` DATETIME NOT NULL,
  `fecha_reembolso` DATE NULL,
  `valor_reembolsado` INT NULL,
  `imagen_comprobante` VARCHAR(100) NULL,
  `reserva_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_reservas_cancelacion_reserva_id`
    FOREIGN KEY (`reserva_id`)
    REFERENCES `reservas_reserva` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`reservas_reserva`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `reservas_reserva`;
CREATE TABLE IF NOT EXISTS `reservas_reserva` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATE NOT NULL,
  `fecha_inicio` DATE NULL,
  `numero_adultos` INT UNSIGNED NOT NULL,
  `numero_menores` INT UNSIGNED NOT NULL,
  `estado` VARCHAR(20) NOT NULL,
  `monto_total` INT NOT NULL,
  `fecha_registro` DATETIME NOT NULL,
  `cliente_id` BIGINT NULL,
  `paquete_id` BIGINT NOT NULL,
  `usuario_id` BIGINT NOT NULL,
  `paquete_promocion_id` BIGINT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `unique_usuario_paquete_fecha_UNIQUE` (`usuario_id`, `paquete_id`, `fecha` ASC),
  UNIQUE INDEX `uq_reservas_reserva_paquete_promocion_id` (`paquete_promocion_id` ASC),
  CONSTRAINT `fk_reservas_reserva_paquete_promocion_id`
    FOREIGN KEY (`paquete_promocion_id`)
    REFERENCES `paquete_promociones` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_reservas_reserva_usuario_id`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `usuarios_usuario` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_reservas_reserva_paquete_id`
    FOREIGN KEY (`paquete_id`)
    REFERENCES `catalogo_paquete` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_reservas_reserva_cliente_id`
    FOREIGN KEY (`cliente_id`)
    REFERENCES `usuarios_cliente` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`seguimiento`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `seguimiento`;
CREATE TABLE IF NOT EXISTS `seguimiento` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `respuesta` TEXT NOT NULL,
  `fecha_respuesta` DATETIME NOT NULL,
  `pqrs_id` BIGINT NOT NULL,
  `usuario_id` BIGINT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_seguimiento_usuario_id`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `usuarios_usuario` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_seguimiento_pqrs_id`
    FOREIGN KEY (`pqrs_id`)
    REFERENCES `comunidad_pqrs` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`seguros_poliza`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `seguros_poliza`;
CREATE TABLE IF NOT EXISTS `seguros_poliza` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre_aseguradora` VARCHAR(100) NOT NULL,
  `descripcion` LONGTEXT NOT NULL,
  `precio_diario` DECIMAL(12, 2) NOT NULL,
  `estado` TINYINT(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`seguros_seguroviaje`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `seguros_seguroviaje`;
CREATE TABLE IF NOT EXISTS `seguros_seguroviaje` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `numero_poliza` VARCHAR(50) NOT NULL,
  `fecha_emision` DATETIME NOT NULL,
  `costo_seguro` DECIMAL(12, 2) NOT NULL,
  `poliza_id` BIGINT NOT NULL,
  `reserva_id` BIGINT NULL,
  `usuario_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uq_seguros_seguroviaje_reserva_id` (`reserva_id` ASC),
  UNIQUE INDEX `uq_seguros_seguroviaje_numero_poliza` (`numero_poliza` ASC),
  CONSTRAINT `fk_seguros_seguroviaje_usuario_id`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `usuarios_usuario` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_seguros_seguroviaje_reserva_id`
    FOREIGN KEY (`reserva_id`)
    REFERENCES `reservas_reserva` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_seguros_seguroviaje_poliza_id`
    FOREIGN KEY (`poliza_id`)
    REFERENCES `seguros_poliza` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`usuarios_cliente`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `usuarios_cliente`;
CREATE TABLE IF NOT EXISTS `usuarios_cliente` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `pais` VARCHAR(100) NOT NULL,
  `departamento` VARCHAR(100) NOT NULL,
  `ciudad` VARCHAR(100) NOT NULL,
  `usuario_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uq_usuarios_cliente_usuario_id` (`usuario_id` ASC),
  CONSTRAINT `fk_usuarios_cliente_usuario_id`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `usuarios_usuario` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`usuarios_guiaturistico`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `usuarios_guiaturistico`;
CREATE TABLE IF NOT EXISTS `usuarios_guiaturistico` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `numero_tarjeta_profesional` VARCHAR(50) NOT NULL,
  `experiencia_anos` INT UNSIGNED NOT NULL,
  `experiencia_fecha` DATE NULL,
  `descripcion_experiencia` LONGTEXT NOT NULL,
  `entidad_salud` VARCHAR(100) NULL,
  `usuario_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uq_usuarios_guiaturistico_usuario_id` (`usuario_id` ASC),
  CONSTRAINT `fk_usuarios_guiaturistico_usuario_id`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `usuarios_usuario` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla `monagua_db`.`usuarios_usuario`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `usuarios_usuario`;
CREATE TABLE IF NOT EXISTS `usuarios_usuario` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `password` VARCHAR(128) NOT NULL,
  `last_login` DATETIME NULL,
  `is_superuser` TINYINT(1) NOT NULL,
  `username` VARCHAR(150) NOT NULL,
  `first_name` VARCHAR(150) NOT NULL,
  `last_name` VARCHAR(150) NOT NULL,
  `is_staff` TINYINT(1) NOT NULL,
  `is_active` TINYINT(1) NOT NULL,
  `date_joined` DATETIME NOT NULL,
  `email` VARCHAR(254) NOT NULL,
  `rol` VARCHAR(20) NOT NULL,
  `tipo_documento` VARCHAR(20) NULL,
  `numero_documento` VARCHAR(20) NULL,
  `telefono` VARCHAR(15) NOT NULL,
  `residencia` VARCHAR(100) NOT NULL,
  `imagen_perfil` VARCHAR(100) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `uq_usuarios_usuario_numero_documento` (`numero_documento` ASC),
  UNIQUE INDEX `uq_usuarios_usuario_email` (`email` ASC),
  UNIQUE INDEX `uq_usuarios_usuario_username` (`username` ASC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- =============================================================================
-- Fin del Script
-- =============================================================================