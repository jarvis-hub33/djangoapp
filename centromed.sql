-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 08-11-2024 a las 02:52:02
-- Versión del servidor: 8.0.31
-- Versión de PHP: 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `centromed`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb3_spanish_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb3_spanish_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb3_spanish_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add Especialidad', 7, 'add_especialidad'),
(26, 'Can change Especialidad', 7, 'change_especialidad'),
(27, 'Can delete Especialidad', 7, 'delete_especialidad'),
(28, 'Can view Especialidad', 7, 'view_especialidad'),
(29, 'Can add Tipo de Atencion', 8, 'add_tipo_atencion'),
(30, 'Can change Tipo de Atencion', 8, 'change_tipo_atencion'),
(31, 'Can delete Tipo de Atencion', 8, 'delete_tipo_atencion'),
(32, 'Can view Tipo de Atencion', 8, 'view_tipo_atencion'),
(33, 'Can add Paciente', 9, 'add_paciente'),
(34, 'Can change Paciente', 9, 'change_paciente'),
(35, 'Can delete Paciente', 9, 'delete_paciente'),
(36, 'Can view Paciente', 9, 'view_paciente');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb3_spanish_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb3_spanish_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb3_spanish_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb3_spanish_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb3_spanish_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$870000$fGOne2rg11z2YkOBPcieaq$zj/6jIbwMuwLL3/jt1+1R0439dhOt1ktj+1je1slZsM=', NULL, 1, 'medadmin', '', '', 'medadmin@correo.cl', 1, 1, '2024-11-05 13:11:29.244481'),
(2, 'pbkdf2_sha256$870000$ifr5Z6lNJmNAOIGwg8eR8A$Iysb8S8OlLErr54vzKGbGU0vaz4FCweNTx9QkDJSOq0=', NULL, 1, 'adminmedico', '', '', 'adminmedico@correo.cl', 1, 1, '2024-11-05 13:12:56.296702'),
(3, 'pbkdf2_sha256$870000$2SZbAJPItcSlmqwr8EUaep$4db4s17aR5ZLmFWa0RvqkNLtRaESIEmlSFSSBqufVcE=', NULL, 1, 'medicoad', '', '', 'medicoad@correo.cl', 1, 1, '2024-11-05 13:16:51.066015'),
(4, 'pbkdf2_sha256$870000$vqsmCkw1efrvIP6qhYpAn0$4w61COwOiF1qQeJZIkGiG8bDrde25hPGJVvKYTOxY1w=', '2024-11-05 16:58:28.248013', 1, 'adminz', '', '', 'adminz@ejemplo.com', 1, 1, '2024-11-05 16:57:51.637051');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_user_id_6a12ed8b` (`user_id`),
  KEY `auth_user_groups_group_id_97559544` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_user_id_a95ead1b` (`user_id`),
  KEY `auth_user_user_permissions_permission_id_1fbb5f2c` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb3_spanish_ci,
  `object_repr` varchar(200) COLLATE utf8mb3_spanish_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext COLLATE utf8mb3_spanish_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6` (`user_id`)
) ;

--
-- Volcado de datos para la tabla `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2024-11-05 16:59:12.736541', '1', 'Medicina General', 1, '[{\"added\": {}}]', 7, 4),
(2, '2024-11-05 16:59:50.468639', '2', 'Pediatria', 1, '[{\"added\": {}}]', 7, 4),
(3, '2024-11-05 17:00:01.604810', '3', 'Dermatologia', 1, '[{\"added\": {}}]', 7, 4),
(4, '2024-11-05 17:00:41.967953', '4', 'Cardiologia', 1, '[{\"added\": {}}]', 7, 4),
(5, '2024-11-05 17:01:55.896369', '1', 'Consulta General', 1, '[{\"added\": {}}]', 8, 4),
(6, '2024-11-05 17:02:06.821747', '2', 'Urgencias', 1, '[{\"added\": {}}]', 8, 4),
(7, '2024-11-05 17:02:15.962782', '3', 'Especializada', 1, '[{\"added\": {}}]', 8, 4),
(8, '2024-11-05 17:02:24.184288', '4', 'Preventiva', 1, '[{\"added\": {}}]', 8, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb3_spanish_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb3_spanish_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'appWeb', 'especialidad'),
(8, 'appWeb', 'tipo_atencion'),
(9, 'appWeb', 'paciente');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb3_spanish_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb3_spanish_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2024-11-05 13:09:16.020221'),
(2, 'auth', '0001_initial', '2024-11-05 13:09:16.472685'),
(3, 'admin', '0001_initial', '2024-11-05 13:09:16.650220'),
(4, 'admin', '0002_logentry_remove_auto_add', '2024-11-05 13:09:16.655251'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2024-11-05 13:09:16.661078'),
(6, 'appWeb', '0001_initial', '2024-11-05 13:09:16.862799'),
(7, 'contenttypes', '0002_remove_content_type_name', '2024-11-05 13:09:16.926094'),
(8, 'auth', '0002_alter_permission_name_max_length', '2024-11-05 13:09:16.963852'),
(9, 'auth', '0003_alter_user_email_max_length', '2024-11-05 13:09:16.996836'),
(10, 'auth', '0004_alter_user_username_opts', '2024-11-05 13:09:17.000849'),
(11, 'auth', '0005_alter_user_last_login_null', '2024-11-05 13:09:17.028774'),
(12, 'auth', '0006_require_contenttypes_0002', '2024-11-05 13:09:17.033040'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2024-11-05 13:09:17.037161'),
(14, 'auth', '0008_alter_user_username_max_length', '2024-11-05 13:09:17.066342'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2024-11-05 13:09:17.092342'),
(16, 'auth', '0010_alter_group_name_max_length', '2024-11-05 13:09:17.120960'),
(17, 'auth', '0011_update_proxy_permissions', '2024-11-05 13:09:17.126931'),
(18, 'auth', '0012_alter_user_first_name_max_length', '2024-11-05 13:09:17.151606'),
(19, 'sessions', '0001_initial', '2024-11-05 13:09:17.192433'),
(20, 'appWeb', '0002_alter_paciente_codigoempleado', '2024-11-05 14:46:13.827972'),
(21, 'appWeb', '0003_alter_paciente_creado', '2024-11-05 17:37:30.988294');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) COLLATE utf8mb3_spanish_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb3_spanish_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('nz7nt2dxa9voj3ti5d4iue2ts2wz7b4y', '.eJxVjDkOwjAUBe_iGlle4o2SPmew_JeQAIqlOKkQd0eWUkD7Zua9RS7HPuej8ZYXElcxiMvvBgWfvHZAj7Leq8S67tsCsivypE2Olfh1O92_g7m0udeWaTApOlU0GIcpopoYOU0OEKLTpNBr75zxEAgC2mSiBksxcVCWxecL85o4Dg:1t8Msu:5lPARWGkDFNRZ35GFWubuUTLQrmF3ZIHL0BEphocObc', '2024-11-19 16:58:28.251067');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `especialidad`
--

DROP TABLE IF EXISTS `especialidad`;
CREATE TABLE IF NOT EXISTS `especialidad` (
  `codigo` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) COLLATE utf8mb3_spanish_ci NOT NULL,
  `creado` datetime(6) NOT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Volcado de datos para la tabla `especialidad`
--

INSERT INTO `especialidad` (`codigo`, `nombre`, `creado`) VALUES
(1, 'Medicina General', '2024-11-05 16:58:38.000000'),
(2, 'Pediatria', '2024-11-05 16:59:15.000000'),
(3, 'Dermatologia', '2024-11-05 16:59:53.000000'),
(4, 'Cardiologia', '2024-11-05 17:00:03.000000');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `paciente`
--

DROP TABLE IF EXISTS `paciente`;
CREATE TABLE IF NOT EXISTS `paciente` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `run` varchar(10) COLLATE utf8mb3_spanish_ci NOT NULL,
  `nombre` varchar(50) COLLATE utf8mb3_spanish_ci NOT NULL,
  `paterno` varchar(50) COLLATE utf8mb3_spanish_ci NOT NULL,
  `materno` varchar(50) COLLATE utf8mb3_spanish_ci NOT NULL,
  `sexo` varchar(1) COLLATE utf8mb3_spanish_ci NOT NULL,
  `codigoEmpleado` varchar(20) COLLATE utf8mb3_spanish_ci NOT NULL,
  `sueldo` int UNSIGNED NOT NULL,
  `fechaNac` date DEFAULT NULL,
  `creado` datetime(6) NOT NULL,
  `especialidad_id` bigint NOT NULL,
  `tipoatencion_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `paciente_especialidad_id_47128c29` (`especialidad_id`),
  KEY `paciente_tipoatencion_id_3a86fa31` (`tipoatencion_id`)
) ;

--
-- Volcado de datos para la tabla `paciente`
--

INSERT INTO `paciente` (`id`, `run`, `nombre`, `paterno`, `materno`, `sexo`, `codigoEmpleado`, `sueldo`, `fechaNac`, `creado`, `especialidad_id`, `tipoatencion_id`) VALUES
(1, '1542-5', 'chala', 'sanchez', 'briceño', 'm', '222222-6', 2323223, '2000-10-01', '2024-11-05 17:39:06.829827', 1, 1),
(2, '323213-2', 'chapulin', 'sanchez', 'Valdivia', 'm', '222323-6', 222222, '1999-12-11', '2024-11-05 19:05:27.514564', 1, 3),
(3, '323213-2', 'chapulin', 'sanchez', 'Valdivia', 'm', '222323-6', 222222, '1999-12-11', '2024-11-05 19:07:50.187590', 1, 3),
(4, '11111111', 'asdksdsa', 'dsdsdd', 'sdsdsds', 'm', '321312-5', 123213123, '1999-12-11', '2024-11-05 19:09:53.807496', 2, 1),
(5, '3432434-5', 'saaaaaa', 'feeeee', 'maaaaa', 'o', '224', 555555, '2000-10-01', '2024-11-05 19:28:28.895178', 2, 2),
(6, '3432434-5', 'saaaaaa', 'feeeee', 'maaaaa', 'o', '224', 555555, '2000-10-01', '2024-11-05 19:29:11.278274', 2, 2),
(7, '3432434-5', 'saaaaaa', 'feeeee', 'maaaaa', 'o', '224', 555555, '2000-10-01', '2024-11-05 19:29:34.606269', 2, 2),
(8, '23232-5', 'siiiipipipi', 'noooo', 'aaaaaa', 'f', '222', 222222, '2000-05-22', '2024-11-05 19:30:09.114983', 1, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipoatencion`
--

DROP TABLE IF EXISTS `tipoatencion`;
CREATE TABLE IF NOT EXISTS `tipoatencion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) COLLATE utf8mb3_spanish_ci NOT NULL,
  `creado` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Volcado de datos para la tabla `tipoatencion`
--

INSERT INTO `tipoatencion` (`id`, `nombre`, `creado`) VALUES
(1, 'Consulta General', '2024-11-05 17:00:47.000000'),
(2, 'Urgencias', '2024-11-05 17:01:57.000000'),
(3, 'Especializada', '2024-11-05 17:02:11.000000'),
(4, 'Preventiva', '2024-11-05 17:02:19.000000');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
