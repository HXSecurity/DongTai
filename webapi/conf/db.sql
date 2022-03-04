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
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `name` (`name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4;

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
  KEY `talent_id` (`talent_id`) USING BTREE,
  CONSTRAINT `auth_department_talent_ibfk_1` FOREIGN KEY (`talent_id`) REFERENCES `auth_talent` (`id`),
  CONSTRAINT `auth_department_talent_ibfk_2` FOREIGN KEY (`department_id`) REFERENCES `auth_department` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `name` (`name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

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
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
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
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
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
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for auth_user_department
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_department`;
CREATE TABLE `auth_user_department` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL COMMENT '用户ID',
  `department_id` int(11) DEFAULT NULL COMMENT '部门ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4;

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
  KEY `group_id` (`group_id`) USING BTREE,
  CONSTRAINT `auth_user_groups_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `auth_user_groups_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4;

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
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
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
  UNIQUE KEY `user_id` (`user_id`) USING BTREE,
  CONSTRAINT `authtoken_token_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
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
) ENGINE=InnoDB AUTO_INCREMENT=2082 DEFAULT CHARSET=utf8mb4;

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
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36314 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=313 DEFAULT CHARSET=utf8mb4;

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
  PRIMARY KEY (`id`) USING BTREE,
  KEY `user_id` (`user_id`) USING BTREE,
  KEY `server_id` (`server_id`) USING BTREE,
  CONSTRAINT `iast_agent_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `iast_agent_ibfk_2` FOREIGN KEY (`server_id`) REFERENCES `iast_server` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=202 DEFAULT CHARSET=utf8mb4;

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
  UNIQUE KEY `pool_sign` (`pool_sign`) USING BTREE,
  KEY `agent_id` (`agent_id`) USING BTREE,
  CONSTRAINT `iast_agent_method_pool_ibfk_1` FOREIGN KEY (`agent_id`) REFERENCES `iast_agent` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1574138 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for iast_agent_method_pool_sinks
-- ----------------------------
DROP TABLE IF EXISTS `iast_agent_method_pool_sinks`;
CREATE TABLE `iast_agent_method_pool_sinks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `methodpool_id` int(11) DEFAULT NULL,
  `hookstrategy_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=205 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

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
  UNIQUE KEY `signature_value` (`signature_value`) USING BTREE,
  KEY `agent_id` (`agent_id`) USING BTREE,
  KEY `level_id` (`level_id`) USING BTREE,
  CONSTRAINT `iast_asset_ibfk_2` FOREIGN KEY (`agent_id`) REFERENCES `iast_agent` (`id`),
  CONSTRAINT `iast_asset_ibfk_3` FOREIGN KEY (`level_id`) REFERENCES `iast_vul_level` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15160 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4;

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
  KEY `agent_id` (`agent_id`) USING BTREE,
  CONSTRAINT `iast_errorlog_ibfk_2` FOREIGN KEY (`agent_id`) REFERENCES `iast_agent` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=94994 DEFAULT CHARSET=utf8mb4;

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
  KEY `agent_id` (`agent_id`) USING BTREE,
  CONSTRAINT `iast_heartbeat_ibfk_2` FOREIGN KEY (`agent_id`) REFERENCES `iast_agent` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1560483 DEFAULT CHARSET=utf8mb4 COMMENT='IAST agent心跳表';

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
) ENGINE=InnoDB AUTO_INCREMENT=500 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=959 DEFAULT CHARSET=utf8mb4;

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
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8mb4;

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
  KEY `scan_id` (`scan_id`) USING BTREE,
  CONSTRAINT `iast_project_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `iast_project_ibfk_2` FOREIGN KEY (`scan_id`) REFERENCES `iast_strategy_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=utf8mb4;

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
  KEY `level_id` (`level_id`) USING BTREE,
  CONSTRAINT `iast_strategy_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `iast_strategy_ibfk_2` FOREIGN KEY (`level_id`) REFERENCES `iast_vul_level` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4;

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
  KEY `user_id` (`user_id`) USING BTREE,
  CONSTRAINT `iast_strategy_user_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4;

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
  KEY `user_id` (`user_id`) USING BTREE,
  CONSTRAINT `iast_system_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

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
  KEY `agent_id` (`agent_id`) USING BTREE,
  CONSTRAINT `iast_vul_overpower_ibfk_2` FOREIGN KEY (`agent_id`) REFERENCES `iast_agent` (`id`)
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
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4;

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
  KEY `level_id` (`level_id`) USING BTREE,
  CONSTRAINT `iast_vulnerability_ibfk_2` FOREIGN KEY (`agent_id`) REFERENCES `iast_agent` (`id`),
  CONSTRAINT `iast_vulnerability_ibfk_3` FOREIGN KEY (`level_id`) REFERENCES `iast_vul_level` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=366 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=39499 DEFAULT CHARSET=utf8mb4;

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
  KEY `aid` (`aid`) USING BTREE,
  CONSTRAINT `sca_maven_artifact_ibfk_1` FOREIGN KEY (`aid`) REFERENCES `sca_artifact_db` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=66971721 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=193562 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=31963 DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;
