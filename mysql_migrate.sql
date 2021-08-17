--
-- Create model User
--
CREATE TABLE `auth_user` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `password` varchar(128) NOT NULL, `last_login` datetime(6) NULL, `username` varchar(150) NOT NULL UNIQUE, `first_name` varchar(150) NOT NULL, `last_name` varchar(150) NOT NULL, `email` varchar(254) NOT NULL, `is_staff` bool NOT NULL, `is_active` bool NOT NULL, `date_joined` datetime(6) NOT NULL, `is_superuser` integer NOT NULL, `phone` varchar(15) NOT NULL);
--
-- Create model HookStrategy
--
CREATE TABLE `iast_hook_strategy` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `value` varchar(255) NULL, `source` varchar(255) NULL, `target` varchar(255) NULL, `inherit` varchar(255) NULL, `track` varchar(5) NULL, `create_time` integer NULL, `update_time` integer NULL, `created_by` integer NULL, `enable` integer NOT NULL);
--
-- Create model HookType
--
CREATE TABLE `iast_hook_type` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `type` integer NULL, `name` varchar(255) NULL, `value` varchar(255) NULL, `enable` integer NULL, `create_time` integer NULL, `update_time` integer NULL, `created_by` integer NULL);
--
-- Create model IastAgent
--
CREATE TABLE `iast_agent` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `token` varchar(255) NULL, `version` varchar(255) NULL, `latest_time` integer NULL, `is_running` integer NULL, `is_core_running` integer NULL, `control` integer NULL, `is_control` integer NULL, `bind_project_id` integer NULL, `project_name` varchar(255) NULL, `online` smallint UNSIGNED NOT NULL, `project_version_id` integer NULL, `language` varchar(10) NULL);
--
-- Create model IastDepartment
--
CREATE TABLE `iast_department` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(255) NULL);
--
-- Create model IastDeployDesc
--
CREATE TABLE `iast_deploy` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `desc` longtext NULL, `middleware` varchar(255) NULL, `language` varchar(255) NULL);
--
-- Create model IastDocument
--
CREATE TABLE `iast_document` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `title` varchar(100) NULL, `url` varchar(100) NULL, `language` varchar(100) NULL, `weight` integer NOT NULL);
--
-- Create model IastOverpowerUserAuth
--
CREATE TABLE `iast_user_auth` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `server_name` varchar(255) NULL, `server_port` varchar(5) NULL, `app_name` varchar(50) NULL, `http_url` varchar(255) NULL, `http_query_string` varchar(2000) NULL, `auth_sql` varchar(255) NULL, `auth_value` varchar(1000) NULL, `jdbc_class` varchar(255) NULL, `created_time` datetime(6) NULL, `updated_time` datetime(6) NULL);
--
-- Create model IastProfile
--
CREATE TABLE `iast_profile` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `key` varchar(100) NOT NULL, `value` varchar(100) NULL);
--
-- Create model IastProject
--
CREATE TABLE `iast_project` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(255) NULL, `mode` varchar(255) NULL, `vul_count` integer UNSIGNED NULL, `agent_count` integer NULL, `latest_time` integer NULL);
--
-- Create model IastServer
--
CREATE TABLE `iast_server` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `hostname` varchar(255) NULL, `ip` varchar(255) NULL, `port` integer NULL, `environment` longtext NULL, `path` varchar(255) NULL, `status` varchar(255) NULL, `container` varchar(255) NULL, `container_path` varchar(255) NULL, `command` varchar(255) NULL, `env` varchar(255) NULL, `runtime` varchar(255) NULL, `create_time` integer NULL, `update_time` integer NULL, `network` varchar(255) NULL, `pid` integer NULL);
--
-- Create model IastVulLevel
--
CREATE TABLE `iast_vul_level` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(255) NULL, `name_value` varchar(255) NULL, `name_type` varchar(255) NULL);
--
-- Create model ScaArtifactDb
--
CREATE TABLE `sca_artifact_db` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `cwe_id` varchar(20) NULL, `cve_id` varchar(20) NULL, `stage` varchar(255) NULL, `title` varchar(255) NULL, `overview` longtext NULL, `teardown` longtext NULL, `group_id` varchar(256) NULL, `artifact_id` varchar(256) NULL, `latest_version` varchar(50) NULL, `component_name` varchar(512) NULL, `dt` integer NULL, `reference` longtext NULL, `cvss_score` double precision NULL, `cvss3_score` double precision NULL, `level` varchar(20) NULL);
--
-- Create model Talent
--
CREATE TABLE `auth_talent` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `talent_name` varchar(255) NOT NULL UNIQUE, `create_time` integer NULL, `update_time` integer NULL, `created_by` integer NULL, `is_active` bool NOT NULL);
--
-- Create model MethodPool
--
CREATE TABLE `iast_agent_method_pool` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `url` varchar(2000) NULL, `uri` varchar(2000) NULL, `http_method` varchar(10) NULL, `http_scheme` varchar(20) NULL, `http_protocol` varchar(255) NULL, `req_header` varchar(2000) NULL, `req_params` varchar(2000) NULL, `req_data` varchar(4000) NULL, `res_header` varchar(1000) NULL, `res_body` varchar(1000) NULL, `req_header_for_search` longtext NULL, `context_path` varchar(255) NULL, `method_pool` longtext NULL, `pool_sign` varchar(40) NULL UNIQUE, `clent_ip` varchar(255) NULL, `create_time` integer NULL, `update_time` integer NULL, `agent_id` integer NULL);
CREATE TABLE `iast_agent_method_pool_sinks` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `methodpool_id` integer NOT NULL, `hookstrategy_id` integer NOT NULL);
--
-- Create model IastVulOverpower
--
CREATE TABLE `iast_vul_overpower` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `http_url` varchar(2000) NULL, `http_uri` varchar(2000) NULL, `http_query_string` varchar(2000) NULL, `http_method` varchar(10) NULL, `http_scheme` varchar(255) NULL, `http_protocol` varchar(255) NULL, `http_header` varchar(2000) NULL, `x_trace_id` varchar(255) NULL, `cookie` varchar(2000) NULL, `sql` varchar(2000) NULL, `created_time` datetime(6) NULL, `updated_time` datetime(6) NULL, `agent_id` integer NULL);
--
-- Create model IastVulnerabilityModel
--
CREATE TABLE `iast_vulnerability` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `type` varchar(255) NULL, `url` varchar(2000) NULL, `uri` varchar(255) NULL, `http_method` varchar(10) NULL, `http_scheme` varchar(255) NULL, `http_protocol` varchar(255) NULL, `req_header` longtext NULL, `req_params` varchar(2000) NULL, `req_data` longtext NULL, `res_header` longtext NULL, `res_body` longtext NULL, `full_stack` longtext NULL, `top_stack` varchar(255) NULL, `bottom_stack` varchar(255) NULL, `taint_value` varchar(255) NULL, `taint_position` varchar(255) NULL, `context_path` varchar(255) NULL, `counts` integer NULL, `status` varchar(255) NULL, `first_time` integer NULL, `latest_time` integer NULL, `client_ip` varchar(255) NULL, `param_name` varchar(255) NULL, `method_pool_id` integer NULL, `agent_id` integer NULL, `level_id` integer NULL);
--
-- Create model IastSystem
--
CREATE TABLE `iast_system` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `agent_value` varchar(50) NULL, `java_version` varchar(50) NULL, `middleware` varchar(50) NULL, `system` varchar(50) NULL, `deploy_status` integer NULL, `created_at` datetime(6) NOT NULL, `update_at` datetime(6) NULL, `user_id` integer NULL);
--
-- Create model IastStrategyUser
--
CREATE TABLE `iast_strategy_user` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(200) NULL, `content` longtext NULL, `status` integer NULL, `created_at` datetime(6) NOT NULL, `user_id` integer NULL);
--
-- Create model IastStrategyModel
--
CREATE TABLE `iast_strategy` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `vul_type` varchar(255) NULL, `state` varchar(255) NULL, `dt` integer NULL, `vul_name` varchar(255) NULL, `vul_desc` longtext NULL, `vul_fix` longtext NULL, `hook_type_id` integer NULL, `level_id` integer NULL, `user_id` integer NULL);
--
-- Create model IastReplayQueue
--
CREATE TABLE `iast_replay_queue` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `relation_id` integer NULL, `state` integer NULL, `count` integer NULL, `result` integer NULL, `create_time` integer NULL, `update_time` integer NULL, `verify_time` integer NULL, `uri` varchar(2000) NULL, `method` varchar(10) NULL, `scheme` varchar(10) NULL, `header` varchar(4000) NULL, `params` varchar(2000) NULL, `body` varchar(4000) NULL, `replay_type` integer NULL, `agent_id` integer NULL);
--
-- Create model IastProjectVersion
--
CREATE TABLE `iast_project_version` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `version_name` varchar(255) NULL, `description` longtext NULL, `current_version` smallint UNSIGNED NOT NULL, `status` smallint UNSIGNED NULL, `create_time` integer NOT NULL, `update_time` integer NOT NULL, `project_id` integer NULL, `user_id` integer NULL);
--
-- Add field scan to iastproject
--
ALTER TABLE `iast_project` ADD COLUMN `scan_id` bigint NULL , ADD CONSTRAINT `iast_project_scan_id_08eb0b8f_fk_iast_strategy_user_id` FOREIGN KEY (`scan_id`) REFERENCES `iast_strategy_user`(`id`);
--
-- Add field user to iastproject
--
ALTER TABLE `iast_project` ADD COLUMN `user_id` integer NULL , ADD CONSTRAINT `iast_project_user_id_c863b2cf_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user`(`id`);
--
-- Create model IastHeartbeat
--
CREATE TABLE `iast_heartbeat` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `memory` varchar(1000) NULL, `cpu` varchar(1000) NULL, `disk` varchar(1000) NULL, `req_count` integer NULL, `dt` integer NULL, `agent_id` integer NULL);
--
-- Create model IastErrorlog
--
CREATE TABLE `iast_errorlog` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `errorlog` longtext NULL, `state` varchar(50) NULL, `dt` integer NULL, `agent_id` integer NULL);
--
-- Create model IastAgentMethodPoolReplay
--
CREATE TABLE `iast_agent_method_pool_replay` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `url` varchar(2000) NULL, `uri` varchar(2000) NULL, `http_method` varchar(10) NULL, `http_scheme` varchar(20) NULL, `http_protocol` varchar(255) NULL, `req_header` varchar(2000) NULL, `req_params` varchar(2000) NULL, `req_data` varchar(4000) NULL, `res_header` varchar(1000) NULL, `res_body` varchar(1000) NULL, `context_path` varchar(255) NULL, `method_pool` longtext NULL, `clent_ip` varchar(255) NULL, `create_time` integer NULL, `update_time` integer NULL, `replay_id` integer NULL, `replay_type` integer NULL, `relation_id` integer NULL, `agent_id` integer NULL);
--
-- Add field server to iastagent
--
ALTER TABLE `iast_agent` ADD COLUMN `server_id` integer NOT NULL , ADD CONSTRAINT `iast_agent_server_id_18c797f1_fk_iast_server_id` FOREIGN KEY (`server_id`) REFERENCES `iast_server`(`id`);
--
-- Add field user to iastagent
--
ALTER TABLE `iast_agent` ADD COLUMN `user_id` integer NOT NULL , ADD CONSTRAINT `iast_agent_user_id_d54d85ea_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user`(`id`);
--
-- Add field type to hookstrategy
--
CREATE TABLE `iast_hook_strategy_type` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `hookstrategy_id` integer NOT NULL, `hooktype_id` integer NOT NULL);
--
-- Create model Department
--
CREATE TABLE `auth_department` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(100) NOT NULL UNIQUE, `create_time` integer NOT NULL, `update_time` integer NOT NULL, `created_by` integer NOT NULL, `parent_id` integer NOT NULL);
CREATE TABLE `auth_department_talent` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `department_id` integer NOT NULL, `talent_id` integer NOT NULL);
--
-- Create model Asset
--
CREATE TABLE `iast_asset` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `package_name` varchar(255) NULL, `package_path` varchar(255) NULL, `signature_algorithm` varchar(255) NULL, `signature_value` varchar(255) NULL, `dt` integer NULL, `version` varchar(255) NULL, `vul_count` integer NULL, `agent_id` integer NULL, `level_id` integer NULL);
--
-- Add field department to user
--
CREATE TABLE `auth_user_department` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `user_id` integer NOT NULL, `department_id` integer NOT NULL);
--
-- Add field groups to user
--
CREATE TABLE `auth_user_groups` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `user_id` integer NOT NULL, `group_id` integer NOT NULL);
--
-- Add field user_permissions to user
--
CREATE TABLE `auth_user_user_permissions` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `user_id` integer NOT NULL, `permission_id` integer NOT NULL);
--
-- Create model ScaMavenArtifact
--
CREATE TABLE `sca_maven_artifact` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `safe_version` varchar(255) NULL, `version_range` varchar(255) NULL, `cph_version` varchar(255) NULL, `dt` integer NULL, `patch` varchar(255) NULL, `cph` varchar(255) NULL, `type` varchar(255) NULL, `group_id` varchar(255) NULL, `artifact_id` varchar(255) NULL, `version` varchar(255) NULL, `signature` varchar(255) NULL, `package_name` varchar(255) NULL, `aid` integer NULL);
ALTER TABLE `sca_artifact_db` ADD CONSTRAINT `sca_artifact_db_cve_id_group_id_artifact_bbb3870d_uniq` UNIQUE (`cve_id`, `group_id`, `artifact_id`, `latest_version`);
ALTER TABLE `iast_agent_method_pool` ADD CONSTRAINT `iast_agent_method_pool_agent_id_30df78eb_fk_iast_agent_id` FOREIGN KEY (`agent_id`) REFERENCES `iast_agent` (`id`);
ALTER TABLE `iast_agent_method_pool_sinks` ADD CONSTRAINT `iast_agent_method_pool_s_methodpool_id_hookstrate_e7e1e2fa_uniq` UNIQUE (`methodpool_id`, `hookstrategy_id`);
ALTER TABLE `iast_agent_method_pool_sinks` ADD CONSTRAINT `iast_agent_method_po_methodpool_id_91970ec9_fk_iast_agen` FOREIGN KEY (`methodpool_id`) REFERENCES `iast_agent_method_pool` (`id`);
ALTER TABLE `iast_agent_method_pool_sinks` ADD CONSTRAINT `iast_agent_method_po_hookstrategy_id_9d25b9fd_fk_iast_hook` FOREIGN KEY (`hookstrategy_id`) REFERENCES `iast_hook_strategy` (`id`);
ALTER TABLE `iast_vul_overpower` ADD CONSTRAINT `iast_vul_overpower_agent_id_755bb185_fk_iast_agent_id` FOREIGN KEY (`agent_id`) REFERENCES `iast_agent` (`id`);
ALTER TABLE `iast_vulnerability` ADD CONSTRAINT `iast_vulnerability_agent_id_a029394b_fk_iast_agent_id` FOREIGN KEY (`agent_id`) REFERENCES `iast_agent` (`id`);
ALTER TABLE `iast_vulnerability` ADD CONSTRAINT `iast_vulnerability_level_id_6382d09e_fk_iast_vul_level_id` FOREIGN KEY (`level_id`) REFERENCES `iast_vul_level` (`id`);
ALTER TABLE `iast_system` ADD CONSTRAINT `iast_system_user_id_c83e80ce_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `iast_strategy_user` ADD CONSTRAINT `iast_strategy_user_user_id_0bddb2a4_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `iast_strategy` ADD CONSTRAINT `iast_strategy_hook_type_id_8dee9a71_fk_iast_hook_type_id` FOREIGN KEY (`hook_type_id`) REFERENCES `iast_hook_type` (`id`);
ALTER TABLE `iast_strategy` ADD CONSTRAINT `iast_strategy_level_id_d5ed00d0_fk_iast_vul_level_id` FOREIGN KEY (`level_id`) REFERENCES `iast_vul_level` (`id`);
ALTER TABLE `iast_strategy` ADD CONSTRAINT `iast_strategy_user_id_4530fb9f_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `iast_replay_queue` ADD CONSTRAINT `iast_replay_queue_agent_id_1c4714cf_fk_iast_agent_id` FOREIGN KEY (`agent_id`) REFERENCES `iast_agent` (`id`);
ALTER TABLE `iast_project_version` ADD CONSTRAINT `iast_project_version_project_id_0a63e2be_fk_iast_project_id` FOREIGN KEY (`project_id`) REFERENCES `iast_project` (`id`);
ALTER TABLE `iast_project_version` ADD CONSTRAINT `iast_project_version_user_id_d52e8faf_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `iast_heartbeat` ADD CONSTRAINT `iast_heartbeat_agent_id_a1d28300_fk_iast_agent_id` FOREIGN KEY (`agent_id`) REFERENCES `iast_agent` (`id`);
ALTER TABLE `iast_errorlog` ADD CONSTRAINT `iast_errorlog_agent_id_1a8a0ccb_fk_iast_agent_id` FOREIGN KEY (`agent_id`) REFERENCES `iast_agent` (`id`);
ALTER TABLE `iast_agent_method_pool_replay` ADD CONSTRAINT `iast_agent_method_pool_replay_agent_id_9799408c_fk_iast_agent_id` FOREIGN KEY (`agent_id`) REFERENCES `iast_agent` (`id`);
ALTER TABLE `iast_hook_strategy_type` ADD CONSTRAINT `iast_hook_strategy_type_hookstrategy_id_hooktype_87f7fb37_uniq` UNIQUE (`hookstrategy_id`, `hooktype_id`);
ALTER TABLE `iast_hook_strategy_type` ADD CONSTRAINT `iast_hook_strategy_t_hookstrategy_id_0cac1cb8_fk_iast_hook` FOREIGN KEY (`hookstrategy_id`) REFERENCES `iast_hook_strategy` (`id`);
ALTER TABLE `iast_hook_strategy_type` ADD CONSTRAINT `iast_hook_strategy_t_hooktype_id_21d98ea3_fk_iast_hook` FOREIGN KEY (`hooktype_id`) REFERENCES `iast_hook_type` (`id`);
ALTER TABLE `auth_department_talent` ADD CONSTRAINT `auth_department_talent_department_id_talent_id_9c5185ea_uniq` UNIQUE (`department_id`, `talent_id`);
ALTER TABLE `auth_department_talent` ADD CONSTRAINT `auth_department_tale_department_id_e0a8f05d_fk_auth_depa` FOREIGN KEY (`department_id`) REFERENCES `auth_department` (`id`);
ALTER TABLE `auth_department_talent` ADD CONSTRAINT `auth_department_talent_talent_id_3ea31765_fk_auth_talent_id` FOREIGN KEY (`talent_id`) REFERENCES `auth_talent` (`id`);
ALTER TABLE `iast_asset` ADD CONSTRAINT `iast_asset_agent_id_effa4b6e_fk_iast_agent_id` FOREIGN KEY (`agent_id`) REFERENCES `iast_agent` (`id`);
ALTER TABLE `iast_asset` ADD CONSTRAINT `iast_asset_level_id_7e3c377d_fk_iast_vul_level_id` FOREIGN KEY (`level_id`) REFERENCES `iast_vul_level` (`id`);
ALTER TABLE `auth_user_department` ADD CONSTRAINT `auth_user_department_user_id_department_id_f26be25b_uniq` UNIQUE (`user_id`, `department_id`);
ALTER TABLE `auth_user_department` ADD CONSTRAINT `auth_user_department_user_id_5b617c46_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `auth_user_department` ADD CONSTRAINT `auth_user_department_department_id_9dc2f123_fk_auth_depa` FOREIGN KEY (`department_id`) REFERENCES `auth_department` (`id`);
ALTER TABLE `auth_user_groups` ADD CONSTRAINT `auth_user_groups_user_id_group_id_94350c0c_uniq` UNIQUE (`user_id`, `group_id`);
ALTER TABLE `auth_user_groups` ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `auth_user_groups` ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);
ALTER TABLE `auth_user_user_permissions` ADD CONSTRAINT `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` UNIQUE (`user_id`, `permission_id`);
ALTER TABLE `auth_user_user_permissions` ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `auth_user_user_permissions` ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);
ALTER TABLE `sca_maven_artifact` ADD CONSTRAINT `sca_maven_artifact_cph_version_aid_35f13689_uniq` UNIQUE (`cph_version`, `aid`);
ALTER TABLE `sca_maven_artifact` ADD CONSTRAINT `sca_maven_artifact_aid_cbbb8971_fk_sca_artifact_db_id` FOREIGN KEY (`aid`) REFERENCES `sca_artifact_db` (`id`);
