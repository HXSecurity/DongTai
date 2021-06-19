/*
 Navicat Premium Data Transfer
 Source Server         : aws-saas-iast
 Source Server Type    : MySQL
 Source Server Version : 50731
 Source Host           : mysql-server:3306
 Source Schema         : iast_webapi
 Target Server Type    : MySQL
 Target Server Version : 50731
 File Encoding         : 65001
 Date: 22/03/2021 18:34:42
*/

CREATE DATABASE if not EXISTS dongtai_webapi
    default character set utf8mb4
    default collate utf8mb4_general_ci;

use dongtai_webapi;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_department
-- ----------------------------
DROP TABLE IF EXISTS `auth_department`;
CREATE TABLE `auth_department` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL COMMENT '部门名称',
  `create_time` int(11) DEFAULT NULL COMMENT '创建时间',
  `update_time` int(11) DEFAULT NULL COMMENT '修改时间',
  `created_by` int(11) DEFAULT NULL COMMENT '创建用户',
  `parent_id` int(11) DEFAULT NULL COMMENT '父节点ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for auth_department_talent
-- ----------------------------
DROP TABLE IF EXISTS `auth_department_talent`;
CREATE TABLE `auth_department_talent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `department_id` int(11) DEFAULT NULL COMMENT '部门ID',
  `talent_id` int(11) DEFAULT NULL COMMENT '租户ID',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `department_id` (`department_id`,`talent_id`) USING BTREE,
  UNIQUE KEY `department_id_2` (`department_id`,`talent_id`) USING BTREE,
  KEY `talent_id` (`talent_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `name` (`name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`) USING BTREE,
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for auth_talent
-- ----------------------------
DROP TABLE IF EXISTS `auth_talent`;
CREATE TABLE `auth_talent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `talent_name` varchar(255) DEFAULT NULL COMMENT '租户名称',
  `create_time` int(11) DEFAULT NULL COMMENT '创建时间',
  `update_time` int(11) DEFAULT NULL COMMENT '修改时间',
  `created_by` int(11) DEFAULT NULL COMMENT '创建用户',
  `is_active` tinyint(1) DEFAULT NULL COMMENT '租户是否启用',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `talent_name` (`talent_name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL COMMENT '0-普通用户、1-系统管理员、2-租户管理员',
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `phone` bigint(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for auth_user_department
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_department`;
CREATE TABLE `auth_user_department` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL COMMENT '用户ID',
  `department_id` int(11) DEFAULT NULL COMMENT '部门ID',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `user_id` (`user_id`),
  KEY `department_id` (`department_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `user_id` (`user_id`) USING BTREE,
  KEY `group_id` (`group_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`) USING BTREE,
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for authtoken_token
-- ----------------------------
DROP TABLE IF EXISTS `authtoken_token`;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`key`) USING BTREE,
  UNIQUE KEY `user_id` (`user_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for captcha_captchastore
-- ----------------------------
DROP TABLE IF EXISTS `captcha_captchastore`;
CREATE TABLE `captcha_captchastore` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `challenge` varchar(32) NOT NULL,
  `response` varchar(32) NOT NULL,
  `hashkey` varchar(40) NOT NULL,
  `expiration` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `hashkey` (`hashkey`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`) USING BTREE,
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
-- ----------------------------
-- Table structure for django_celery_beat_clockedschedule
-- ----------------------------
DROP TABLE IF EXISTS `django_celery_beat_clockedschedule`;
CREATE TABLE `django_celery_beat_clockedschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `clocked_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for django_celery_beat_crontabschedule
-- ----------------------------
DROP TABLE IF EXISTS `django_celery_beat_crontabschedule`;
CREATE TABLE `django_celery_beat_crontabschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `minute` varchar(240) NOT NULL,
  `hour` varchar(96) NOT NULL,
  `day_of_week` varchar(64) NOT NULL,
  `day_of_month` varchar(124) NOT NULL,
  `month_of_year` varchar(64) NOT NULL,
  `timezone` varchar(63) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for django_celery_beat_intervalschedule
-- ----------------------------
DROP TABLE IF EXISTS `django_celery_beat_intervalschedule`;
CREATE TABLE `django_celery_beat_intervalschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `every` int(11) NOT NULL,
  `period` varchar(24) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

BEGIN;
INSERT INTO `django_celery_beat_intervalschedule`(`id`, `every`, `period`) VALUES (1, 10, 'seconds');
INSERT INTO `django_celery_beat_intervalschedule`(`id`, `every`, `period`) VALUES (2, 1, 'hours');
INSERT INTO `django_celery_beat_intervalschedule`(`id`, `every`, `period`) VALUES (3, 5, 'minutes');
INSERT INTO `django_celery_beat_intervalschedule`(`id`, `every`, `period`) VALUES (4, 1, 'days');
INSERT INTO `django_celery_beat_intervalschedule`(`id`, `every`, `period`) VALUES (5, 30, 'days');
COMMIT;

-- ----------------------------
-- Table structure for django_celery_beat_periodictask
-- ----------------------------
DROP TABLE IF EXISTS `django_celery_beat_periodictask`;
CREATE TABLE `django_celery_beat_periodictask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `task` varchar(200) NOT NULL,
  `args` longtext NOT NULL,
  `kwargs` longtext NOT NULL,
  `queue` varchar(200) DEFAULT NULL,
  `exchange` varchar(200) DEFAULT NULL,
  `routing_key` varchar(200) DEFAULT NULL,
  `expires` datetime(6) DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `last_run_at` datetime(6) DEFAULT NULL,
  `total_run_count` int(10) unsigned NOT NULL,
  `date_changed` datetime(6) NOT NULL,
  `description` longtext NOT NULL,
  `crontab_id` int(11) DEFAULT NULL,
  `interval_id` int(11) DEFAULT NULL,
  `solar_id` int(11) DEFAULT NULL,
  `one_off` tinyint(1) NOT NULL,
  `start_time` datetime(6) DEFAULT NULL,
  `priority` int(10) unsigned DEFAULT NULL,
  `headers` longtext NOT NULL,
  `clocked_id` int(11) DEFAULT NULL,
  `expire_seconds` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `name` (`name`) USING BTREE,
  KEY `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` (`crontab_id`) USING BTREE,
  KEY `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` (`interval_id`) USING BTREE,
  KEY `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` (`solar_id`) USING BTREE,
  KEY `django_celery_beat_p_clocked_id_47a69f82_fk_django_ce` (`clocked_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

BEGIN;
INSERT INTO `django_celery_beat_periodictask`(`id`, `name`, `task`, `args`, `kwargs`, `queue`, `exchange`, `routing_key`, `expires`, `enabled`, `last_run_at`, `total_run_count`, `date_changed`, `description`, `crontab_id`, `interval_id`, `solar_id`, `one_off`, `start_time`, `priority`, `headers`, `clocked_id`, `expire_seconds`) VALUES (2, 'engine.heartbeat', 'core.tasks.heartbeat', '[]', '{}', NULL, NULL, NULL, NULL, 1, '2021-05-08 05:34:02.743450', 509, '2021-05-08 05:35:33.100817', '', NULL, 2, NULL, 0, NULL, NULL, '{}', NULL, NULL);
INSERT INTO `django_celery_beat_periodictask`(`id`, `name`, `task`, `args`, `kwargs`, `queue`, `exchange`, `routing_key`, `expires`, `enabled`, `last_run_at`, `total_run_count`, `date_changed`, `description`, `crontab_id`, `interval_id`, `solar_id`, `one_off`, `start_time`, `priority`, `headers`, `clocked_id`, `expire_seconds`) VALUES (3, 'engine.update_agent_status', 'core.tasks.update_agent_status', '[]', '{}', NULL, NULL, NULL, NULL, 1, '2021-05-08 06:25:47.527645', 2509, '2021-05-08 06:27:22.947828', '', NULL, 3, NULL, 0, NULL, NULL, '{}', NULL, NULL);
INSERT INTO `django_celery_beat_periodictask`(`id`, `name`, `task`, `args`, `kwargs`, `queue`, `exchange`, `routing_key`, `expires`, `enabled`, `last_run_at`, `total_run_count`, `date_changed`, `description`, `crontab_id`, `interval_id`, `solar_id`, `one_off`, `start_time`, `priority`, `headers`, `clocked_id`, `expire_seconds`) VALUES (4, 'engine.update_sca', 'core.tasks.update_sca', '[]', '{}', NULL, NULL, NULL, NULL, 1, '2021-05-08 06:25:35.184066', 8, '2021-05-08 06:27:22.926700', '', NULL, 4, NULL, 0, NULL, NULL, '{}', NULL, NULL);
COMMIT;

-- ----------------------------
-- Table structure for django_celery_beat_periodictasks
-- ----------------------------
DROP TABLE IF EXISTS `django_celery_beat_periodictasks`;
CREATE TABLE `django_celery_beat_periodictasks` (
  `ident` smallint(6) NOT NULL,
  `last_update` datetime(6) NOT NULL,
  PRIMARY KEY (`ident`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for django_celery_beat_solarschedule
-- ----------------------------
DROP TABLE IF EXISTS `django_celery_beat_solarschedule`;
CREATE TABLE `django_celery_beat_solarschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event` varchar(24) NOT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `django_celery_beat_solar_event_latitude_longitude_ba64999a_uniq` (`event`,`latitude`,`longitude`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  KEY `django_session_expire_date_a5c62663` (`expire_date`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for iast_agent
-- ----------------------------
DROP TABLE IF EXISTS `iast_agent`;
CREATE TABLE `iast_agent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(255) DEFAULT NULL COMMENT 'agent唯一标识',
  `version` varchar(255) DEFAULT NULL COMMENT '版本',
  `latest_time` int(11) DEFAULT NULL COMMENT '更新时间',
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `server_id` int(11) DEFAULT NULL COMMENT '服务器ID',
  `is_running` int(1) DEFAULT NULL COMMENT 'agent运行状态',
  `control` int(1) DEFAULT NULL COMMENT 'agent控制位，1-安装、2-卸载、0-无控制',
  `is_control` int(1) DEFAULT NULL COMMENT '是否正处于控制中，0-否，1-是',
  `bind_project_id` int(11) DEFAULT '0' COMMENT '捆绑项目ID，存在则为已捆绑',
  `project_name` varchar(255) DEFAULT NULL COMMENT '项目名称，用于先启动agent后创建项目',
  `project_version_id` int(11) NULL DEFAULT 0 COMMENT '项目版本ID',
  `online` tinyint(4) NULL DEFAULT 0 COMMENT '1在线运行，0未运行，同token，仅一个online',
  `is_core_running` int(11) NULL DEFAULT NULL COMMENT '核心引擎是否启动',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `user_id` (`user_id`) USING BTREE,
  KEY `server_id` (`server_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for iast_agent_method_pool
-- ----------------------------
DROP TABLE IF EXISTS `iast_agent_method_pool`;
CREATE TABLE `iast_agent_method_pool` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `agent_id` int(11) DEFAULT NULL COMMENT 'Agent',
  `url` varchar(2000) DEFAULT NULL COMMENT 'URL',
  `uri` varchar(2000) DEFAULT NULL COMMENT 'URI',
  `http_method` varchar(10) DEFAULT NULL COMMENT 'HTTP请求方法',
  `http_scheme` varchar(20) DEFAULT NULL COMMENT '协议',
  `http_protocol` varchar(255) DEFAULT NULL COMMENT 'HTTP协议',
  `req_header` varchar(2000) DEFAULT NULL COMMENT '请求头',
  `req_params` varchar(2000) DEFAULT NULL COMMENT '请求参数',
  `req_data` varchar(4000) DEFAULT NULL COMMENT '请求体',
  `res_header` varchar(1000) DEFAULT NULL COMMENT '响应头',
  `res_body` varchar(1000) DEFAULT NULL COMMENT '响应体',
  `context_path` varchar(255) DEFAULT NULL COMMENT '应用上下文',
  `language` varchar(20) DEFAULT NULL COMMENT '语言',
  `method_pool` json DEFAULT NULL COMMENT '方法池',
  `clent_ip` varchar(255) DEFAULT NULL COMMENT '客户端IP',
  `create_time` int(11) DEFAULT NULL COMMENT '创建时间',
  `update_time` int(11) DEFAULT NULL COMMENT '修改时间',
  `pool_sign` varchar(40) DEFAULT NULL COMMENT '方法池签名',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `pool_sign` (`pool_sign`,`agent_id`) USING BTREE,
  KEY `agent_id` (`agent_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for iast_agent_method_pool_sinks
-- ----------------------------
DROP TABLE IF EXISTS `iast_agent_method_pool_sinks`;
CREATE TABLE `iast_agent_method_pool_sinks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `methodpool_id` int(11) DEFAULT NULL,
  `hookstrategy_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `methodpool_id` (`methodpool_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for iast_agent_properties
-- ----------------------------
DROP TABLE IF EXISTS `iast_agent_properties`;
CREATE TABLE `iast_agent_properties` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `hook_type` int(1) DEFAULT '0' COMMENT 'HOOK类型，1-全量HOOK，0-按配置HOOK',
  `dump_class` int(1) DEFAULT '0' COMMENT '是否dump修改后的字节码，1-dump，0-不dump，默认不dump',
  `create_time` int(11) DEFAULT NULL COMMENT '创建时间',
  `update_time` int(11) DEFAULT NULL COMMENT '修改时间',
  `updated_by` int(11) DEFAULT NULL COMMENT '修改人',
  `agent_id` int(11) DEFAULT NULL COMMENT 'agent',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for iast_asset
-- ----------------------------
DROP TABLE IF EXISTS `iast_asset`;
CREATE TABLE `iast_asset` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `package_name` varchar(255) DEFAULT NULL COMMENT '第三方包名',
  `package_path` varchar(255) DEFAULT NULL COMMENT '第三方包所在路径',
  `signature_algorithm` varchar(255) DEFAULT NULL COMMENT '签名算法',
  `signature_value` varchar(50) DEFAULT NULL COMMENT '签名值',
  `dt` int(11) DEFAULT NULL COMMENT '更新时间',
  `version` varchar(255) DEFAULT NULL COMMENT '当前版本',
  `level_id` int(11) DEFAULT NULL COMMENT '漏洞等级',
  `vul_count` int(11) DEFAULT NULL COMMENT '漏洞数量',
  `agent_id` int(11) DEFAULT NULL COMMENT 'agent id',
  `language` varchar(255) DEFAULT NULL COMMENT '语言',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `signature_value` (`signature_value`,`agent_id`) USING HASH,
  KEY `agent_id` (`agent_id`) USING BTREE,
  KEY `level_id` (`level_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for iast_deploy
-- ----------------------------
DROP TABLE IF EXISTS `iast_deploy`;
CREATE TABLE `iast_deploy` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `desc` mediumtext COMMENT '安装描述',
  `middleware` varchar(255) DEFAULT NULL COMMENT '中间件',
  `os` varchar(255) DEFAULT NULL COMMENT '操作系统',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

BEGIN;
INSERT INTO `iast_deploy`(`id`, `desc`, `middleware`, `os`) VALUES (1, '**手动修改**\n\n进入tomcat主目录，找到`bin/catalina.sh`文件，在**文件首行**增加如下配置：\n```bash\nCATALINA_OPTS=-javaagent:/path/to/server/agent.jar\" \"-Dproject.name=<project name>\n```\n\n**注意：**`<project name>`与创建的项目名称保持一致，agent将自动关联至项目；如果不配置该参数，需要进入项目管理中进行手工绑定。', 'tomcat', 'linux');
INSERT INTO `iast_deploy`(`id`, `desc`, `middleware`, `os`) VALUES (2, '####  JBossAS 6\n\n进入JBoss容器的主目录，在`bin/run.sh`文件中找到`# Setup JBoss specific properties`所在行，在该行的下面插入如下行：\n```bash\nJAVA_OPTS=\"$JAVA_OPTS \"-javaagent:/path/to/server/agent.jar\" \"-Dproject.name=<project name>\n```\n**注意：**`<project name>`与创建的项目名称保持一致，agent将自动关联至项目；如果不配置该参数，需要进入项目管理中进行手工绑定。\n\n\n#### JBossAS 7、JBossWildfly\n\n进入JBoss容器的主目录，根据当前服务器的启动类型：standalone、domain修改对应的配置文件\n\n##### Standalone模式\n打开`bin/standalone.sh`文件，定位`# Display our environment`所在的行，在其上方插入自定义配置，如下：\n```bash\nJAVA_OPTS=\"$JAVA_OPTS \"-javaagent:/path/to/server/agent.jar\" \"-Dproject.name=<project name>\n```\n**注意：**`<project name>`与创建的项目名称保持一致，agent将自动关联至项目；如果不配置该参数，需要进入项目管理中进行手工绑定。\n\n##### domain模式\ndomain模式下的部署方式与Standalone模式类似，请自行查询', 'jboss', 'linux');
INSERT INTO `iast_deploy`(`id`, `desc`, `middleware`, `os`) VALUES (3, '> Jetty\n#### 手工修改\n1.进入jetty的根目录，打开`bin/jetty.sh`文件，找到`Add jetty properties to Java VM options.`所在行，在下面行插入`JAVA_OPTIONS+=( \"-javaagent:/opt/agent/agent.jar=token=e7509bf7-e44f-4e1f-8e25-5079e2540c63\")`\n\n2.重启jetty服务器\n\n#### 自动修改\n进入tomcat容器的主目录，找到`bin/jetty.sh`文件，使用下面的shell命令修改jetty.sh文件\n```bash\nsed \"$(cat jetty.sh |grep -n \\\"Add jetty properties to Java VM options\\\"|cut -d \":\" -f1) aJAVA_OPTS=\\\"\\$JAVA_OPTS\\ \\\"-javaagent:/opt/agent/agent.jar=token=e7509bf7-e44f-4e1f-8e25-5079e2540c63\" -i jetty.sh\n```', 'jetty', 'linux');
INSERT INTO `iast_deploy`(`id`, `desc`, `middleware`, `os`) VALUES (4, '> Resin\n#### 手动修改\n进入resin容器的主目录，打开`conf/cluster-default.xml`文件，定位到`<server-default>`所在的行，在该行下面插入`<jvm-arg>-javaagent:/opt/agent/agent.jar</jvm-arg>`', 'resin', 'linux');
INSERT INTO `iast_deploy`(`id`, `desc`, `middleware`, `os`) VALUES (5, '> WebLogic配置agent\n\n#### 手动修改\n**非集群方式**\n\n进入WebLogic目录，打开`bin/startWebLogic.sh`文件，找到`JAVA_OPTIONS=\"${SAVE_JAVA_OPTIONS}\"`所在行，在该行的下面增加一行\n\n```\nJAVA_OPTIONS=\"-javaagent:${DOMAIN_HOME}/agent/agent.jar\"\n```\n\n**集群方式**\n\n##### 方式一、通过weblogic的console\n\n访问weblogic的console，例如：\n\n1.找到“环境”下的“服务器”，然后在服务器列表中点击需要安装agent的服务器，如：AdminServer\n\n![img](https://i0x0fy4ibf.feishu.cn/space/api/box/stream/download/asynccode/?code=6920cd75d5484b9dcae5f67a8aad155f_8f118824ce50c961_boxcngZyBvKQSo849VNXlQBJuge_YuAYCtHZdJXJCwvIlL3fxPrHcOQuN1Ce)\n\n2.进入服务器详情，点击“服务器启动”，在下方的参数一栏中填入javaagent的参数`-javaagent:/opt/agent/agent.jar`，如：\n\n![img](https://i0x0fy4ibf.feishu.cn/space/api/box/stream/download/asynccode/?code=e32f0fdef6dc3e199632ee96e9e14aa5_8f118824ce50c961_boxcnfxBALg44nqZNvWICeYo93f_mfxihZ670SCKmxtDiZ3ykAkC556TiWMW)\n\n3.重启服务器，使配置生效\n\n![img](https://i0x0fy4ibf.feishu.cn/space/api/box/stream/download/asynccode/?code=346e5344abca7fae8d3cdc89c05f2fbd_8f118824ce50c961_boxcn3SbZEAQhl0B4RSMJpZbibv_o17TRySNfvsOwiyoAYdmpC7GU9XmegU4)\n\n\n\n##### 方式二、通过配置weblogic的config.xml文件\n\n找到`/u01/oracle/weblogic/user_projects/domains/base_domain/config`目录下的config.xml文件，定位到`<server-start>`标签下的`<arguments>`标签，在标签内添加如下配置：\n```\n-javaagent:/opt/agent/agent.jar\n```\n\n\n', 'weblogic', 'linux');
INSERT INTO `iast_deploy`(`id`, `desc`, `middleware`, `os`) VALUES (6, '> WebSphere\n![websphere-01](/upload/masterimg/websphere-01.png)\n![websphere-02](/upload/masterimg/websphere-02.png)\n![websphere-03](/upload/masterimg/websphere-03.png)\n', 'websphere', 'linux');
INSERT INTO `iast_deploy`(`id`, `desc`, `middleware`, `os`) VALUES (7, '> WebLogic\n![weblogic-01](/upload/masterimg/weblogic-01.png)\n![weblogic-02](/upload/masterimg/weblogic-02.png)\n![weblogic-03](/upload/masterimg/weblogic-03.png)\n![weblogic-04](/upload/masterimg/weblogic-04.png)', 'weblogic', 'windows');
INSERT INTO `iast_deploy`(`id`, `desc`, `middleware`, `os`) VALUES (8, '**SpringBoot**\n\n1. 下载`agent.jar`，然后放入具有写入权限的目录中，如：`/tmp/`\n\n2. 针对SpringBoot应用\n	1). 如果使用**war包**的方式部署，agent的安装方式为具体中间件的安装方式\n	2). 如果使用`java -jar app.jar`的方式部署，则直接在启动命令中增加启动参数`-javaagent:/path/to/agent.jar`即可，如：`java -javaagent:/path/to/agent.jar -Dproject.name=<project name> -jar app.jar`\n	\n**注意：**`<project name>`与创建的项目名称保持一致，agent将自动关联至项目；如果不配置该参数，需要进入项目管理中进行手工绑定。', 'SpringBoot', 'linux');
INSERT INTO `iast_deploy`(`id`, `desc`, `middleware`, `os`) VALUES (10, '**SpringBoot**\n\n1. 下载`agent.jar`，然后放入具有写入权限的目录中，如：`/tmp/`\n\n2. 针对SpringBoot应用\n	1）如果使用**war包**的方式部署，agent的安装方式为具体中间件的安装方式；\n	2）如果使用`java -jar app.jar`的方式部署，则直接在启动命令中增加启动参数`-javaagent:/path/to/agent.jar`即可，如：`java -javaagent:/path/to/agent.jar -Dproject.name=<project name> -jar app.jar`\n	\n**注意：**`<project name>`与创建的项目名称保持一致，agent将自动关联至项目；如果不配置该参数，需要进入项目管理中进行手工绑定。', 'SpringBoot', 'windows');
COMMIT;

-- ----------------------------
-- Table structure for iast_engine_heartbeat
-- ----------------------------
DROP TABLE IF EXISTS `iast_engine_heartbeat`;
CREATE TABLE `iast_engine_heartbeat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_ip` varchar(255) DEFAULT NULL COMMENT '客户端IP',
  `status` varchar(255) DEFAULT NULL COMMENT '引擎状态',
  `msg` varchar(255) DEFAULT NULL COMMENT '引擎返回信息',
  `agentCount` int(11) DEFAULT NULL COMMENT '历史agent数量',
  `reqCount` bigint(255) DEFAULT NULL COMMENT '历史请求数量',
  `agentEnableCount` int(11) DEFAULT NULL COMMENT '正在运行的agent数量',
  `projectCount` int(11) DEFAULT NULL COMMENT '项目数量',
  `userCount` int(11) DEFAULT NULL COMMENT '用户数量',
  `vulCount` int(11) DEFAULT NULL COMMENT '漏洞数量',
  `methodPoolCount` int(11) DEFAULT NULL COMMENT '方法池数量',
  `timestamp` int(11) DEFAULT NULL COMMENT '时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for iast_errorlog
-- ----------------------------
DROP TABLE IF EXISTS `iast_errorlog`;
CREATE TABLE `iast_errorlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `errorlog` mediumtext COMMENT '错误日志详情',
  `state` varchar(50) DEFAULT NULL COMMENT '错误日志状态',
  `dt` int(11) DEFAULT NULL COMMENT '日志触发时间',
  `agent_id` int(11) DEFAULT NULL COMMENT 'agent id',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `agent_id` (`agent_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for iast_heartbeat
-- ----------------------------
DROP TABLE IF EXISTS `iast_heartbeat`;
CREATE TABLE `iast_heartbeat` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `hostname` varchar(1000) DEFAULT NULL COMMENT '主机名',
  `network` varchar(2000) DEFAULT NULL COMMENT '网卡信息 ',
  `memory` varchar(1000) DEFAULT NULL COMMENT '内存信息',
  `cpu` varchar(1000) DEFAULT NULL COMMENT 'CPU信息',
  `disk` varchar(1000) DEFAULT NULL COMMENT '磁盘信息',
  `pid` varchar(1050) DEFAULT NULL COMMENT '进程ID，带主机名',
  `env` mediumtext COMMENT '环境变量',
  `req_count` int(255) DEFAULT NULL COMMENT 'HTTP请求数量',
  `dt` int(11) DEFAULT NULL COMMENT '最近一次心跳时间',
  `agent_id` int(11) DEFAULT NULL COMMENT 'agent ID',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `agent_id` (`agent_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='IAST agent心跳表';

-- ----------------------------
-- Table structure for iast_hook_strategy
-- ----------------------------
DROP TABLE IF EXISTS `iast_hook_strategy`;
CREATE TABLE `iast_hook_strategy` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `value` varchar(2000) DEFAULT NULL COMMENT '策略值',
  `source` varchar(255) DEFAULT NULL COMMENT '污点来源',
  `target` varchar(255) DEFAULT NULL COMMENT '污点去向',
  `inherit` varchar(255) DEFAULT NULL COMMENT '继承类型，false-仅检测当前类，true-进检测子类，all-检测当前类及子类',
  `track` varchar(5) DEFAULT NULL COMMENT '是否需要污点跟踪，true-需要，false-不需要',
  `create_time` int(11) DEFAULT NULL COMMENT '创建时间',
  `update_time` int(11) DEFAULT NULL COMMENT '修改时间',
  `created_by` int(11) DEFAULT NULL COMMENT '创建人',
  `enable` tinyint(1) DEFAULT '1' COMMENT '启用状态：0-禁用，1-启用，-1-删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for iast_hook_strategy_type
-- ----------------------------
DROP TABLE IF EXISTS `iast_hook_strategy_type`;
CREATE TABLE `iast_hook_strategy_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `hookstrategy_id` int(11) DEFAULT NULL COMMENT '策略ID',
  `hooktype_id` int(11) DEFAULT NULL COMMENT '策略类型ID',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `hookstrategy_id` (`hookstrategy_id`,`hooktype_id`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for iast_hook_talent_strategy
-- ----------------------------
DROP TABLE IF EXISTS `iast_hook_talent_strategy`;
CREATE TABLE `iast_hook_talent_strategy` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `talent_id` int(11) DEFAULT NULL COMMENT '租户ID',
  `values` varchar(500) DEFAULT NULL COMMENT '租户启用的策略类型',
  `create_time` int(11) DEFAULT NULL COMMENT '创建时间',
  `update_time` int(11) DEFAULT NULL COMMENT '修改时间',
  `created_by` int(11) DEFAULT NULL COMMENT '创建者',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `talent_id` (`talent_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for iast_hook_type
-- ----------------------------
DROP TABLE IF EXISTS `iast_hook_type`;
CREATE TABLE `iast_hook_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` int(11) DEFAULT NULL COMMENT '策略总类型，1-source节点、2-propagator节点、3-filter节点、4-sink节点',
  `name` varchar(255) DEFAULT NULL COMMENT '策略类型名称',
  `value` varchar(255) DEFAULT NULL COMMENT '策略类型值',
  `enable` int(1) DEFAULT NULL COMMENT '状态：1-启用；0-禁用',
  `create_time` int(11) DEFAULT NULL COMMENT '创建时间',
  `update_time` int(11) DEFAULT NULL COMMENT '修改时间',
  `created_by` int(11) DEFAULT NULL COMMENT '创建者',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for iast_notify_config
-- ----------------------------
DROP TABLE IF EXISTS `iast_notify_config`;
CREATE TABLE `iast_notify_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notify_type` int(11) DEFAULT NULL COMMENT '通知类型，webhook、jira、dingding、企业微信等',
  `notify_metadata` json DEFAULT NULL COMMENT '通知相关的元数据，包括，账号、密码、模版等数据',
  `user_id` int(11) DEFAULT NULL COMMENT '用户ID',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for iast_project
-- ----------------------------
DROP TABLE IF EXISTS `iast_project`;
CREATE TABLE `iast_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL COMMENT '项目名称',
  `mode` varchar(255) DEFAULT NULL COMMENT '项目类型，默认为插桩',
  `vul_count` int(11) unsigned DEFAULT '0' COMMENT '漏洞数量',
  `agent_count` int(11) DEFAULT NULL COMMENT 'Agent数量',
  `latest_time` int(11) DEFAULT NULL COMMENT '最新时间',
  `user_id` int(11) DEFAULT NULL COMMENT 'user id',
  `scan_id` bigint(20) unsigned DEFAULT NULL COMMENT '扫描策略ID',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `user_id` (`user_id`) USING BTREE,
  KEY `scan_id` (`scan_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for iast_project_version
-- ----------------------------
CREATE TABLE `iast_project_version`  (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `version_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '版本号名称',
  `project_id` int(11) NULL DEFAULT NULL COMMENT '项目ID',
  `current_version` tinyint(4) NULL DEFAULT 0 COMMENT '1当前版本0预备版本',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '版本描述',
  `status` tinyint(4) NULL DEFAULT 1 COMMENT '1有效数据0无效',
  `create_time` int(11) NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` int(11) NULL DEFAULT NULL COMMENT '更新时间',
  `user_id` int(11) NULL DEFAULT NULL COMMENT 'user id',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `id`(`id`) USING BTREE,
  INDEX `project_id`(`project_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for iast_server
-- ----------------------------
DROP TABLE IF EXISTS `iast_server`;
CREATE TABLE `iast_server` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `name` varchar(255) DEFAULT NULL COMMENT '服务器名称',
  `hostname` varchar(255) DEFAULT NULL COMMENT '主机名',
  `ip` varchar(255) DEFAULT NULL COMMENT '服务器IP地址',
  `port` int(11) DEFAULT NULL COMMENT '服务器开放的端口',
  `environment` text COMMENT '运行环境：dev/test/prod',
  `agent_version` varchar(20) DEFAULT NULL COMMENT 'Agent版本',
  `latest_agent_version` varchar(255) DEFAULT NULL COMMENT '最新Agent版本',
  `language` varchar(20) DEFAULT NULL COMMENT 'Agent语言',
  `path` varchar(255) DEFAULT NULL COMMENT '服务器路径',
  `status` varchar(255) DEFAULT NULL COMMENT '服务器状态',
  `container` varchar(255) DEFAULT NULL COMMENT '中间件信息',
  `container_path` varchar(255) DEFAULT NULL COMMENT '中间件路径',
  `command` varchar(255) DEFAULT NULL COMMENT '启动命令',
  `env` varchar(255) DEFAULT NULL COMMENT '环境变量',
  `runtime` varchar(255) DEFAULT NULL COMMENT '运行时环境',
  `create_time` int(11) DEFAULT NULL COMMENT '启动时间',
  `update_time` int(11) DEFAULT NULL COMMENT '最近一次活跃',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for iast_strategy
-- ----------------------------
DROP TABLE IF EXISTS `iast_strategy`;
CREATE TABLE `iast_strategy` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `user_id` int(11) DEFAULT NULL COMMENT '用户ID',
  `vul_type` varchar(255) DEFAULT NULL COMMENT '漏洞类型',
  `level_id` int(11) DEFAULT NULL COMMENT '漏洞等级',
  `state` varchar(255) DEFAULT NULL COMMENT '策略状态，true-开启，false-关闭',
  `dt` int(11) DEFAULT NULL COMMENT '策略变更时间',
  `vul_name` varchar(255) DEFAULT NULL COMMENT '漏洞名称（中文）',
  `vul_desc` text COMMENT '漏洞描述',
  `vul_fix` text COMMENT '修复建议',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `user_id` (`user_id`) USING BTREE,
  KEY `level_id` (`level_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

BEGIN;
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (1, 1, 'cmd-injection', 1, 'enable', 1, '命令注入', '命令注入漏洞是指由于Web应用程序对用户提交的数据过滤不严格，导致黑客可以通过构造特殊命令字符串的方式，将数据提交至Web应用程序中，并利用该方式执行外部程序或系统命令实施攻击，非法获取数据或者网络资源等。', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (2, 1, 'smtp-injection', 1, 'enable', 1, 'SMTP注入', '攻击者利用IMAP / SMTP服务器上输入验证的弱点在服务器上执行命令。Web邮件服务器通常位于Internet与IMAP或SMTP邮件服务器之间。Web邮件服务器接收到用户请求，然后Web邮件服务器向后端邮件服务器查询所请求的信息，并将此响应返回给用户。在IMAP / SMTP命令注入攻击中，邮件服务器命令嵌入在发送到Web邮件服务器的部分请求中。如果Web邮件服务器未能充分清理这些请求，则当Web邮件服务器查询后端服务器时，这些命令将被发送到后端邮件服务器，然后在此处执行命令。', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (3, 1, 'ssrf', 1, 'enable', 1, '服务器端请求伪造', '将请求中的参数`<<<result_vul.information.probe.vulparam>>>`的内容设置为测试Payload:`<<<result_vul.information.probe.poc>>>`后进行分析发现<<<result_vul.information.description>>>，故判定该请求存在<<<vultags.tag_title>>>\r\n请求信息:\r\n```http<<=http-result_vul.information.probe=>>```\r\n响应信息:\r\n```http<<=httpresponse-result_vul.information.response=>>```', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (4, 1, 'unsafe-xml-decode', 1, 'enable', 1, '不安全的XML Decode', '当用户输入以不安全的方式插入到服务器端XML文档或SOAP消息中时，就会XML外部实体注入漏洞。恶意用户可构造XML元自付破坏XML原本结构，从而查看应用服务器本地文件或对应用同一网络环境下的应用进行间接攻击。', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (5, 1, 'sql-injection', 1, 'enable', 1, 'SQL注入', '软件使用来自上游组件的外部影响的输入来构造全部或部分SQL命令，但不会中和或不正确地中和了特殊元素，这些特殊元素在将其发送到下游组件时可能会修改预期的SQL命令。', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (6, 1, 'ldap-injection', 1, 'enable', 1, 'LDAP注入', 'LDAP注入是指客户端发送查询请求时，输入的字符串中含有一些特殊字符，导致修改了LDAP本来的查询结构，从而使得可以访问更多的未授权数据的一种攻击方式。', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (7, 1, 'xpath-injection', 1, 'enable', 1, 'XPATH注入', 'XPath注入攻击，是指利用XPath 解析器的松散输入和容错特性，能够在 URL、表单或其它信息上附带恶意的XPath 查询代码，以获得权限信息的访问权并更改这些信息。XPath注入攻击是针对Web服务应用新的攻击方法，它允许攻击者在事先不知道XPath查询相关知 识的情况下，通过XPath查询得到一个XML文档的完整内容。Xpath注入攻击本质上和SQL注入攻击是类似的，都是输入一些恶意的查询等代码字符串，从而对网站进行攻击。', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (8, 1, 'path-traversal', 1, 'enable', 1, '路径穿越', 'CWE-23，该软件使用外部输入来构建路径名，该路径名应位于受限目录内，但不能正确中和诸如“ ..”之类的序列，这些序列可以解析到该目录之外的位置。', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (9, 1, 'crypto-weak-randomness', 3, 'enable', 1, '弱随机数算法', '随机数在计算机应用中使用的比较广泛，最为熟知的便是在密码学中的应用。随机数分为真随机数和伪随机数，我们程序使用的基本都是伪随机数。伪随机又分为强伪随机数和弱伪随机数。伪随机数，通过一定算法和种子得出。软件实现的是伪随机数。强伪随机数，难以预测的随机数。弱伪随机数，易于预测的随机数。\nJava程序中，使用java.util.Random获得随机数，这种随机数源于伪随机数生成器，产生的随机数容易被预测，对于安全性要求较高的环境中，使用这种随机数可能会降低系统安全性，使攻击者有机可乘。', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (10, 1, 'crypto-bad-mac', 3, 'enable', 1, '弱哈希算法', '哈希算法是使用哈希函数将任意长度的消息映射成为一个长度较短且长度固定的值，这个经过映射的值为哈希值。它是一种单向加密体制，即一个从明文到密文的不可逆映射，只有加密过程，没有解密过程。而不安全的哈希算法则可以逆向推出明文。在密码学中，哈希算法主要用于消息摘要和签名来对整个消息的完整性进行校验，所以需要哈希算法无法推导输入的原始值，这是哈希算法安全性的基础。目前常用的哈希算法包括MD4、MD5、SHA等。本篇文章以JAVA语言源代码为例，分析不安全的哈希算法缺陷产生的原因以及修复方法。详细请参见：CWE ID 327: Use of a Broken or Risky Cryptographic Algorithm (http://cwe.mitre.org/data/definitions/327.html)。', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (11, 1, 'crypto-bad-cipher', 3, 'enable', 1, '弱加密算法', '数据通过弱加密算法MessageDigest函数进行加密', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (12, 1, 'cookie-flags-missing', 3, 'enable', 1, 'Cookie未设置secure', '没有设置HTTPS会话中敏感cookie的安全属性，这可能导致用户代理通过HTTP会话以明文发送这些cookie。', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (13, 1, 'trust-boundary-violation', 3, 'enable', 1, '信任边界', 'CWE-501，信任边界可以认为是通过程序绘制的线。 在生产线的一侧，数据不受信任。 在该行的另一端，假定数据是可信的。 验证逻辑的目的是允许数据安全地越过信任边界-从不受信任变为受信任。 当程序模糊了可信和不可信之间的界限时，就会发生信任边界冲突。 通过在同一数据结构中组合可信数据和不可信数据，程序员可以更容易地错误地信任未验证的数据。', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (14, 1, 'reflected-xss', 2, 'enable', 1, '反射型xss', '跨站脚本攻击漏洞简称XSS漏洞,主要是由于应用后端未对用户输入进行安全校验或校验不严格导致恶意用户可自定义控制页面输出内容，从而产生跨站脚本攻击漏洞。通常来说恶意用户通过构造闭合标签方式在HTML页面中插入Javascript代码，在正常用户浏览此页面时对正常用户进行攻击，常见的攻击方式有获取用户的身份凭据、对用户内网进行探测扫描、执行钓鱼欺骗攻击等', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (15, 1, 'header-injection', 3, 'enable', 1, 'Header头注入', 'HTTP响应拆分漏洞，也叫CRLF注入攻击。CR、LF分别对应回车、换行字符。攻击者可能注入自定义HTTP头。例如，攻击者可以注入会话cookie或HTML代码。这可能会进行类似的XSS（跨站点脚本）或会话固定漏洞。', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (16, 1, 'hql-injection', 1, 'enable', 1, 'HQL注入', 'CWE-564，使用Hibernate执行使用用户控制的输入构建的动态SQL语句，可使攻击者修改该语句的含义或执行任意SQL命令。', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (17, 1, 'unsafe-readline', 3, 'enable', 1, '不安全的readline', '使用不安全的方法进行行数据读取', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (18, 1, 'expression-language-injection', 1, 'enable', 1, '表达式注入', 'CWE-917，该软件使用来自上游组件的外部影响的输入来构造Java Server Page（JSP）中的全部或部分表达语言（EL）语句，但不会中和或错误地中和了可以修改预期的EL语句的特殊元素。它被执行。', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (19, 1, 'redos', 3, 'enable', 1, '正则DOS', 'CWE-185，使用的正则表达式会导致数据不正确的匹配或比较，造成程序响应速度变慢', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (20, 1, 'reflection-injection', 1, 'enable', 1, '反射注入', '使用反射方式动态加载用户输入的类名，如果未做过滤，可加载恶意类产生命令执行等风险。', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (21, 1, 'nosql-injection', 1, 'enable', 1, 'NoSql注入', 'NoSQL(泛指非关系型的数据库)注入是指服务端充分信任用户输入导致输入带入查询操作，导致用户可控制数据库查询语句；但由于nosql数据库不同于传统数据库的语法，由于各个数据库之间使用语法、API一般不同，NoSQL注入攻击可能在应用程序的不同区域执行，具体取决于使用的NoSQL API和数据模型；NoSQL注入按照攻击途径又分五类：重言式/永真式、联合查询、JavaScript注入、背负式查询、跨域违规；', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (22, 1, 'unvalidated-redirect', 3, 'enable', 1, '不安全的重定向', 'CWE-601，Web应用程序接受用户控制的输入，该输入指定到外部站点的链接，并在重定向中使用该链接，简化了网络钓鱼攻击。', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (23, 1, 'unvalidated-forward', 3, 'enable', 1, '不安全的转发', '验证服务端是否使用不受信任的数据链接进行重定向。', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (24, 1, 'crypto-bad-ciphers', 3, 'enable', 1, '弱加密算法', '数据通过弱加密算法MessageDigest函数进行加密', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (25, 1, 'dynamic-library-load', 1, 'enable', 1, 'JNI注入', 'JNI注入是指由于WEB应用程序对用户提交的JNI包过滤不严格，导致攻击者可以通过构造恶意JNI包并动态加载至WEB应用中', '这里是修复建议');
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (26, 1, 'xxe', 2, 'enable', 1, 'XXE', 'XML 指可扩展标记语言（eXtensible Markup Language），是一种用于标记电子文件使其具有结构性的标记语言，被设计用来传输和存储数据。XML文档结构包括XML声明、DTD文档类型定义（可选）、文档元素。目前，XML文件作为配置文件（Spring、Struts2等）、文档结构说明文件（PDF、RSS等）、图片格式文件（SVG header）应用比较广泛。 XML 的语法规范由 DTD （Document Type Definition）来进行控制。\n\nXML外部实体注入（XML External Entity Injection）漏洞是指当恶意用户在提交一个精心构造的包含外部实体引用的XML文档给未正确配置的XML解析器处理时，该攻击就会发生。', NULL);
INSERT INTO `iast_strategy`(`id`, `user_id`, `vul_type`, `level_id`, `state`, `dt`, `vul_name`, `vul_desc`, `vul_fix`) VALUES (27, 1, 'unsafe-json-deserialize', 1, 'enable', 1, '不安全的JSON反序列化', '不安全的JSON反序列化是指WEB应用程序对用户提交的反序列化数据未进行有效过滤，导致反序列化过程中产生命令执行、文件读取等漏洞', NULL);
COMMIT;

-- ----------------------------
-- Table structure for iast_strategy_user
-- ----------------------------
DROP TABLE IF EXISTS `iast_strategy_user`;
CREATE TABLE `iast_strategy_user` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL COMMENT '策略名称',
  `content` text COMMENT '策略ID串',
  `user_id` int(11) DEFAULT NULL COMMENT '用户ID',
  `status` tinyint(2) DEFAULT '1' COMMENT '1有效0无效',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `id` (`id`) USING BTREE,
  KEY `user_id` (`user_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for iast_system
-- ----------------------------
DROP TABLE IF EXISTS `iast_system`;
CREATE TABLE `iast_system` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `agent_value` varchar(50) DEFAULT NULL COMMENT 'agent类型',
  `java_version` varchar(50) DEFAULT NULL COMMENT 'java版本',
  `middleware` varchar(50) DEFAULT NULL COMMENT '中间件',
  `system` varchar(50) DEFAULT NULL COMMENT '系统信息',
  `deploy_status` tinyint(5) DEFAULT NULL COMMENT '0未安装，1第一步，2第二部',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `user_id` int(11) DEFAULT NULL COMMENT '操作用户',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `id` (`id`) USING BTREE,
  KEY `user_id` (`user_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for iast_vul_level
-- ----------------------------
DROP TABLE IF EXISTS `iast_vul_level`;
CREATE TABLE `iast_vul_level` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL COMMENT '漏洞等级名称 ：high、medium、low、info',
  `name_value` varchar(255) DEFAULT NULL COMMENT '漏洞等级值：高危、中危、低危、提示',
  `name_type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

BEGIN;
INSERT INTO `iast_vul_level`(`id`, `name`, `name_value`, `name_type`) VALUES (1, 'high', '高危', '高危漏洞');
INSERT INTO `iast_vul_level`(`id`, `name`, `name_value`, `name_type`) VALUES (2, 'medium', '中危', '中危漏洞');
INSERT INTO `iast_vul_level`(`id`, `name`, `name_value`, `name_type`) VALUES (3, 'low', '低危', '低危漏洞');
INSERT INTO `iast_vul_level`(`id`, `name`, `name_value`, `name_type`) VALUES (4, 'info', '提示', '提示信息');
COMMIT;

-- ----------------------------
-- Table structure for iast_vul_overpower
-- ----------------------------
DROP TABLE IF EXISTS `iast_vul_overpower`;
CREATE TABLE `iast_vul_overpower` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `agent_id` int(255) DEFAULT NULL COMMENT 'agent ID ',
  `http_url` varchar(2000) DEFAULT NULL COMMENT 'HTTP请求的URL',
  `http_uri` varchar(2000) DEFAULT NULL COMMENT 'HTTP请求的URI',
  `http_query_string` varchar(2000) DEFAULT NULL COMMENT 'HTTP请求的查询参数',
  `http_method` varchar(10) DEFAULT NULL COMMENT 'HTTP请求的方法',
  `http_scheme` varchar(255) DEFAULT NULL COMMENT 'HTTP请求的协议',
  `http_protocol` varchar(255) DEFAULT NULL COMMENT 'HTTP请求协议（完整）',
  `http_header` varchar(2000) DEFAULT NULL COMMENT 'HTTP请求头',
  `x_trace_id` varchar(255) DEFAULT NULL COMMENT '灵芝trace-id',
  `cookie` varchar(2000) DEFAULT NULL COMMENT '当前请求的cookie',
  `sql` varchar(2000) DEFAULT NULL COMMENT '当前请求触发的sql语句',
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `agent_id` (`agent_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for iast_vul_rule
-- ----------------------------
DROP TABLE IF EXISTS `iast_vul_rule`;
CREATE TABLE `iast_vul_rule` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `rule_name` varchar(255) DEFAULT NULL COMMENT '策略名称',
  `rule_level` varchar(10) DEFAULT NULL COMMENT '策略等级',
  `rule_msg` varchar(255) DEFAULT NULL COMMENT '策略描述',
  `rule_value` json DEFAULT NULL COMMENT '策略详情',
  `is_enable` tinyint(1) DEFAULT NULL COMMENT '是否启用，0-禁用、1-启用',
  `is_system` tinyint(1) DEFAULT NULL COMMENT '是否为系统策略',
  `create_by` int(11) DEFAULT NULL COMMENT '创建者',
  `create_time` int(11) DEFAULT NULL COMMENT '创建时间',
  `update_time` int(11) DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `rule_name` (`rule_name`,`create_by`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for iast_vulnerability
-- ----------------------------
DROP TABLE IF EXISTS `iast_vulnerability`;
CREATE TABLE `iast_vulnerability` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `type` varchar(255) DEFAULT NULL COMMENT '漏洞类型',
  `level_id` int(11) DEFAULT NULL COMMENT '漏洞等级',
  `url` varchar(2000) DEFAULT NULL COMMENT '漏洞url',
  `uri` varchar(255) DEFAULT '' COMMENT 'uri',
  `http_method` varchar(10) DEFAULT NULL COMMENT '漏洞请求方法',
  `http_scheme` varchar(255) DEFAULT NULL COMMENT '协议名',
  `http_protocol` varchar(255) DEFAULT NULL COMMENT 'HTTP协议',
  `req_header` mediumtext COMMENT '漏洞请求的header头',
  `req_params` varchar(2000) DEFAULT NULL COMMENT '漏洞url的get参数',
  `req_data` mediumtext COMMENT '漏洞url的post数据信息',
  `res_header` mediumtext COMMENT '漏洞响应头',
  `res_body` mediumtext COMMENT '漏洞响应包',
  `full_stack` mediumtext COMMENT '漏洞栈',
  `top_stack` varchar(255) DEFAULT NULL COMMENT '污点栈-栈顶',
  `bottom_stack` varchar(255) DEFAULT NULL COMMENT '污点栈-栈底',
  `taint_value` varchar(255) DEFAULT NULL COMMENT '污点值',
  `taint_position` varchar(255) DEFAULT NULL COMMENT '漏洞所在请求的位置',
  `agent_id` int(11) DEFAULT '0' COMMENT '应用ID',
  `context_path` varchar(255) DEFAULT NULL COMMENT '漏洞所在应用',
  `counts` int(11) DEFAULT NULL COMMENT '漏洞出现次数',
  `status` varchar(255) DEFAULT NULL COMMENT '漏洞状态：已上报、已确认、已忽略',
  `language` varchar(255) DEFAULT NULL COMMENT '开发语言',
  `first_time` int(11) DEFAULT NULL COMMENT '漏洞第一次出现的时间',
  `latest_time` int(11) DEFAULT NULL COMMENT '漏洞最近一次出现的时间',
  `client_ip` varchar(255) DEFAULT NULL COMMENT '来源IP',
  `param_name` varchar(255) DEFAULT NULL COMMENT '传递参数变量名称',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `agent_id` (`agent_id`) USING BTREE,
  KEY `level_id` (`level_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for sca_artifact_db
-- ----------------------------
DROP TABLE IF EXISTS `sca_artifact_db`;
CREATE TABLE `sca_artifact_db` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `cwe_id` varchar(20) DEFAULT NULL COMMENT 'CWE漏洞编号',
  `cve_id` varchar(20) DEFAULT NULL COMMENT 'CVE漏洞编号',
  `stage` varchar(255) DEFAULT NULL COMMENT '第三方包发布类型',
  `title` varchar(255) DEFAULT NULL COMMENT '漏洞标题',
  `overview` text COMMENT '漏洞概述',
  `teardown` text COMMENT '漏洞详细解释（markdown）',
  `group_id` varchar(256) DEFAULT NULL COMMENT '第三方组件的组信息',
  `artifact_id` varchar(256) DEFAULT NULL COMMENT '第三方组件的名称',
  `latest_version` varchar(50) DEFAULT NULL COMMENT '第三方组件的最新版本',
  `component_name` varchar(512) DEFAULT NULL COMMENT '第三方组件的human名称',
  `dt` int(11) DEFAULT NULL COMMENT '数据添加时间',
  `reference` text COMMENT '相关链接/分析文章',
  `cvss_score` float(10,0) DEFAULT NULL COMMENT 'cvss2评分',
  `cvss3_score` float(10,0) DEFAULT NULL COMMENT 'cvss3评分',
  `level` varchar(20) DEFAULT NULL COMMENT '漏洞等级(以cvss3为准）',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `cve_id` (`cve_id`,`group_id`,`artifact_id`,`latest_version`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for sca_maven_artifact
-- ----------------------------
DROP TABLE IF EXISTS `sca_maven_artifact`;
CREATE TABLE `sca_maven_artifact` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `aid` int(11) DEFAULT NULL COMMENT 'artifactdb表关联主键',
  `safe_version` varchar(255) DEFAULT NULL COMMENT '推荐版本',
  `version_range` varchar(255) DEFAULT NULL COMMENT '组件版本范围',
  `cph_version` varchar(255) DEFAULT NULL COMMENT 'maven查询规范',
  `dt` int(11) DEFAULT NULL COMMENT '更新时间',
  `patch` varchar(255) DEFAULT NULL COMMENT '补丁地址',
  `cph` varchar(255) DEFAULT NULL COMMENT '组件maven查询语法',
  `type` varchar(255) DEFAULT NULL COMMENT '包管理器类型',
  `group_id` varchar(255) DEFAULT NULL COMMENT '包管理器组',
  `artifact_id` varchar(255) DEFAULT NULL COMMENT 'artifact',
  `version` varchar(255) DEFAULT NULL COMMENT '版本',
  `signature` varchar(255) DEFAULT NULL COMMENT '版本哈希',
  `package_name` varchar(255) DEFAULT NULL COMMENT '包名',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `cph_version` (`cph_version`,`aid`) USING BTREE,
  KEY `aid` (`aid`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for sca_maven_db
-- ----------------------------
DROP TABLE IF EXISTS `sca_maven_db`;
CREATE TABLE `sca_maven_db` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `group_id` varchar(255) DEFAULT NULL COMMENT 'Java第三方组件的groupID',
  `atrifact_id` varchar(255) DEFAULT NULL COMMENT 'Java第三方组件的ArtifactId',
  `version` varchar(255) DEFAULT NULL COMMENT 'Java第三方组件的版本号',
  `sha_1` varchar(255) DEFAULT NULL COMMENT 'Java包的SHA-1值，用于与灵芝Agent获取的数据进行匹配',
  `package_name` varchar(255) DEFAULT NULL COMMENT '包名',
  `aql` varchar(255) DEFAULT NULL COMMENT '组件查询语言',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `sha_1` (`sha_1`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for sca_record
-- ----------------------------
DROP TABLE IF EXISTS `sca_record`;
CREATE TABLE `sca_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `page` int(11) DEFAULT NULL COMMENT '当前页',
  `total` int(11) DEFAULT NULL COMMENT '总页数',
  `dt` int(11) DEFAULT NULL COMMENT '更新时间s',
  `type` varchar(255) DEFAULT NULL COMMENT '记录类型',
  `data` varchar(255) DEFAULT NULL COMMENT '记录数据',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for sca_vul_db
-- ----------------------------
DROP TABLE IF EXISTS `sca_vul_db`;
CREATE TABLE `sca_vul_db` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `package_type` varchar(20) DEFAULT NULL COMMENT '包管理器',
  `cve` varchar(20) DEFAULT NULL COMMENT 'cve编号',
  `cwe` varchar(20) DEFAULT NULL COMMENT 'cwe编号',
  `vul_name` varchar(255) DEFAULT NULL COMMENT '漏洞名称',
  `vul_level` varchar(20) DEFAULT NULL COMMENT '漏洞等级',
  `cve_href` varchar(255) DEFAULT NULL COMMENT 'CVE地址',
  `cwe_href` varchar(255) DEFAULT NULL COMMENT 'CWE地址',
  `aql` varchar(255) DEFAULT NULL COMMENT '组件查询语言：',
  `version_range` varchar(255) DEFAULT NULL COMMENT '版本范围',
  `version_condition` varchar(255) DEFAULT NULL COMMENT '版本范围-条件',
  `latest_version` varchar(255) DEFAULT NULL COMMENT '最新版本',
  `overview` varchar(255) DEFAULT NULL COMMENT '漏洞概述',
  `teardown` varchar(2000) DEFAULT NULL COMMENT '漏洞详细描述',
  `url` varchar(255) DEFAULT NULL COMMENT '漏洞地址',
  `source` varchar(20) DEFAULT NULL COMMENT '数据来源',
  `dt` int(11) DEFAULT NULL COMMENT '时间戳',
  `extra` varchar(2000) DEFAULT NULL COMMENT '附加数据，暂时不知道是否有用',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `package_type` (`package_type`,`cve`,`cwe`,`vul_name`,`aql`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

BEGIN;
-- 创建默认用户
INSERT INTO `auth_user`(`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `phone`) VALUES (1, 'pbkdf2_sha256$180000$tpUFyXYrIGXh$PIqkgklZerTwKsDe5s9P+6USI/Z2Yq+5J6oXx4kbiKI=', '2021-03-23 18:32:44.117558', 1, 'admin', 'admin', 'admin', 'admin@huoxian.cn', 1, 1, '2020-01-01 00:00:00.000000', 1);

-- 创建租户
INSERT INTO `auth_talent`(`id`, `talent_name`, `create_time`, `update_time`, `created_by`, `is_active`) VALUES (1, '默认租户', 1610532209, 1611031026, 1, 1);

-- 创建部门
INSERT INTO `auth_department`(`id`, `name`, `create_time`, `update_time`, `created_by`, `parent_id`) VALUES (1, '默认部门', 1611031807, 1611045352, 1, -1);

-- 创建组
INSERT INTO `auth_group`(`id`, `name`) VALUES (1, 'system_admin');
INSERT INTO `auth_group`(`id`, `name`) VALUES (5, 'talent_admin');
INSERT INTO `auth_group`(`id`, `name`) VALUES (2, 'user');

-- 创建关联关系
INSERT INTO `auth_department_talent`(`id`, `department_id`, `talent_id`) VALUES (1, 1, 1);
INSERT INTO `auth_user_department`(`id`, `user_id`, `department_id`) VALUES (1, 1, 1);
INSERT INTO `auth_user_groups`(`id`, `user_id`, `group_id`) VALUES (1, 1, 1);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
