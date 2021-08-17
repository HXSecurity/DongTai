BEGIN;
--
-- Create model User
--
CREATE TABLE "auth_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "username" varchar(150) NOT NULL UNIQUE, "first_name" varchar(150) NOT NULL, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "is_superuser" integer NOT NULL, "phone" varchar(15) NOT NULL);
--
-- Create model HookStrategy
--
CREATE TABLE "iast_hook_strategy" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "value" varchar(255) NULL, "source" varchar(255) NULL, "target" varchar(255) NULL, "inherit" varchar(255) NULL, "track" varchar(5) NULL, "create_time" integer NULL, "update_time" integer NULL, "created_by" integer NULL, "enable" integer NOT NULL);
--
-- Create model HookType
--
CREATE TABLE "iast_hook_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "type" integer NULL, "name" varchar(255) NULL, "value" varchar(255) NULL, "enable" integer NULL, "create_time" integer NULL, "update_time" integer NULL, "created_by" integer NULL);
--
-- Create model IastAgent
--
CREATE TABLE "iast_agent" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "token" varchar(255) NULL, "version" varchar(255) NULL, "latest_time" integer NULL, "is_running" integer NULL, "is_core_running" integer NULL, "control" integer NULL, "is_control" integer NULL, "bind_project_id" integer NULL, "project_name" varchar(255) NULL, "online" smallint unsigned NOT NULL CHECK ("online" >= 0), "project_version_id" integer NULL, "language" varchar(10) NULL);
--
-- Create model IastDepartment
--
CREATE TABLE "iast_department" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(255) NULL);
--
-- Create model IastDeployDesc
--
CREATE TABLE "iast_deploy" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "desc" text NULL, "middleware" varchar(255) NULL, "language" varchar(255) NULL);
--
-- Create model IastDocument
--
CREATE TABLE "iast_document" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NULL, "url" varchar(100) NULL, "language" varchar(100) NULL, "weight" integer NOT NULL);
--
-- Create model IastOverpowerUserAuth
--
CREATE TABLE "iast_user_auth" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "server_name" varchar(255) NULL, "server_port" varchar(5) NULL, "app_name" varchar(50) NULL, "http_url" varchar(255) NULL, "http_query_string" varchar(2000) NULL, "auth_sql" varchar(255) NULL, "auth_value" varchar(1000) NULL, "jdbc_class" varchar(255) NULL, "created_time" datetime NULL, "updated_time" datetime NULL);
--
-- Create model IastProfile
--
CREATE TABLE "iast_profile" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "key" varchar(100) NOT NULL, "value" varchar(100) NULL);
--
-- Create model IastProject
--
CREATE TABLE "iast_project" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(255) NULL, "mode" varchar(255) NULL, "vul_count" integer unsigned NULL CHECK ("vul_count" >= 0), "agent_count" integer NULL, "latest_time" integer NULL);
--
-- Create model IastServer
--
CREATE TABLE "iast_server" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "hostname" varchar(255) NULL, "ip" varchar(255) NULL, "port" integer NULL, "environment" text NULL, "path" varchar(255) NULL, "status" varchar(255) NULL, "container" varchar(255) NULL, "container_path" varchar(255) NULL, "command" varchar(255) NULL, "env" varchar(255) NULL, "runtime" varchar(255) NULL, "create_time" integer NULL, "update_time" integer NULL, "network" varchar(255) NULL, "pid" integer NULL);
--
-- Create model IastVulLevel
--
CREATE TABLE "iast_vul_level" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(255) NULL, "name_value" varchar(255) NULL, "name_type" varchar(255) NULL);
--
-- Create model ScaArtifactDb
--
CREATE TABLE "sca_artifact_db" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "cwe_id" varchar(20) NULL, "cve_id" varchar(20) NULL, "stage" varchar(255) NULL, "title" varchar(255) NULL, "overview" text NULL, "teardown" text NULL, "group_id" varchar(256) NULL, "artifact_id" varchar(256) NULL, "latest_version" varchar(50) NULL, "component_name" varchar(512) NULL, "dt" integer NULL, "reference" text NULL, "cvss_score" real NULL, "cvss3_score" real NULL, "level" varchar(20) NULL);
--
-- Create model Talent
--
CREATE TABLE "auth_talent" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "talent_name" varchar(255) NOT NULL UNIQUE, "create_time" integer NULL, "update_time" integer NULL, "created_by" integer NULL, "is_active" bool NOT NULL);
--
-- Create model MethodPool
--
CREATE TABLE "iast_agent_method_pool" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "url" varchar(2000) NULL, "uri" varchar(2000) NULL, "http_method" varchar(10) NULL, "http_scheme" varchar(20) NULL, "http_protocol" varchar(255) NULL, "req_header" varchar(2000) NULL, "req_params" varchar(2000) NULL, "req_data" varchar(4000) NULL, "res_header" varchar(1000) NULL, "res_body" varchar(1000) NULL, "req_header_for_search" text NULL, "context_path" varchar(255) NULL, "method_pool" text NULL, "pool_sign" varchar(40) NULL UNIQUE, "clent_ip" varchar(255) NULL, "create_time" integer NULL, "update_time" integer NULL, "agent_id" integer NULL REFERENCES "iast_agent" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "iast_agent_method_pool_sinks" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "methodpool_id" integer NOT NULL REFERENCES "iast_agent_method_pool" ("id") DEFERRABLE INITIALLY DEFERRED, "hookstrategy_id" integer NOT NULL REFERENCES "iast_hook_strategy" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model IastVulOverpower
--
CREATE TABLE "iast_vul_overpower" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "http_url" varchar(2000) NULL, "http_uri" varchar(2000) NULL, "http_query_string" varchar(2000) NULL, "http_method" varchar(10) NULL, "http_scheme" varchar(255) NULL, "http_protocol" varchar(255) NULL, "http_header" varchar(2000) NULL, "x_trace_id" varchar(255) NULL, "cookie" varchar(2000) NULL, "sql" varchar(2000) NULL, "created_time" datetime NULL, "updated_time" datetime NULL, "agent_id" integer NULL REFERENCES "iast_agent" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model IastVulnerabilityModel
--
CREATE TABLE "iast_vulnerability" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "type" varchar(255) NULL, "url" varchar(2000) NULL, "uri" varchar(255) NULL, "http_method" varchar(10) NULL, "http_scheme" varchar(255) NULL, "http_protocol" varchar(255) NULL, "req_header" text NULL, "req_params" varchar(2000) NULL, "req_data" text NULL, "res_header" text NULL, "res_body" text NULL, "full_stack" text NULL, "top_stack" varchar(255) NULL, "bottom_stack" varchar(255) NULL, "taint_value" varchar(255) NULL, "taint_position" varchar(255) NULL, "context_path" varchar(255) NULL, "counts" integer NULL, "status" varchar(255) NULL, "first_time" integer NULL, "latest_time" integer NULL, "client_ip" varchar(255) NULL, "param_name" varchar(255) NULL, "method_pool_id" integer NULL, "agent_id" integer NULL REFERENCES "iast_agent" ("id") DEFERRABLE INITIALLY DEFERRED, "level_id" integer NULL REFERENCES "iast_vul_level" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model IastSystem
--
CREATE TABLE "iast_system" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "agent_value" varchar(50) NULL, "java_version" varchar(50) NULL, "middleware" varchar(50) NULL, "system" varchar(50) NULL, "deploy_status" integer NULL, "created_at" datetime NOT NULL, "update_at" datetime NULL, "user_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model IastStrategyUser
--
CREATE TABLE "iast_strategy_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NULL, "content" text NULL, "status" integer NULL, "created_at" datetime NOT NULL, "user_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model IastStrategyModel
--
CREATE TABLE "iast_strategy" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "vul_type" varchar(255) NULL, "state" varchar(255) NULL, "dt" integer NULL, "vul_name" varchar(255) NULL, "vul_desc" text NULL, "vul_fix" text NULL, "hook_type_id" integer NULL REFERENCES "iast_hook_type" ("id") DEFERRABLE INITIALLY DEFERRED, "level_id" integer NULL REFERENCES "iast_vul_level" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model IastReplayQueue
--
CREATE TABLE "iast_replay_queue" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "relation_id" integer NULL, "state" integer NULL, "count" integer NULL, "result" integer NULL, "create_time" integer NULL, "update_time" integer NULL, "verify_time" integer NULL, "uri" varchar(2000) NULL, "method" varchar(10) NULL, "scheme" varchar(10) NULL, "header" varchar(4000) NULL, "params" varchar(2000) NULL, "body" varchar(4000) NULL, "replay_type" integer NULL, "agent_id" integer NULL REFERENCES "iast_agent" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model IastProjectVersion
--
CREATE TABLE "iast_project_version" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "version_name" varchar(255) NULL, "description" text NULL, "current_version" smallint unsigned NOT NULL CHECK ("current_version" >= 0), "status" smallint unsigned NULL CHECK ("status" >= 0), "create_time" integer NOT NULL, "update_time" integer NOT NULL, "project_id" integer NULL REFERENCES "iast_project" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Add field scan to iastproject
--
CREATE TABLE "new__iast_project" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(255) NULL, "mode" varchar(255) NULL, "vul_count" integer unsigned NULL CHECK ("vul_count" >= 0), "agent_count" integer NULL, "latest_time" integer NULL, "scan_id" bigint NULL REFERENCES "iast_strategy_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__iast_project" ("id", "name", "mode", "vul_count", "agent_count", "latest_time", "scan_id") SELECT "id", "name", "mode", "vul_count", "agent_count", "latest_time", NULL FROM "iast_project";
DROP TABLE "iast_project";
ALTER TABLE "new__iast_project" RENAME TO "iast_project";
CREATE UNIQUE INDEX "sca_artifact_db_cve_id_group_id_artifact_id_latest_version_bbb3870d_uniq" ON "sca_artifact_db" ("cve_id", "group_id", "artifact_id", "latest_version");
CREATE INDEX "iast_agent_method_pool_agent_id_30df78eb" ON "iast_agent_method_pool" ("agent_id");
CREATE UNIQUE INDEX "iast_agent_method_pool_sinks_methodpool_id_hookstrategy_id_e7e1e2fa_uniq" ON "iast_agent_method_pool_sinks" ("methodpool_id", "hookstrategy_id");
CREATE INDEX "iast_agent_method_pool_sinks_methodpool_id_91970ec9" ON "iast_agent_method_pool_sinks" ("methodpool_id");
CREATE INDEX "iast_agent_method_pool_sinks_hookstrategy_id_9d25b9fd" ON "iast_agent_method_pool_sinks" ("hookstrategy_id");
CREATE INDEX "iast_vul_overpower_agent_id_755bb185" ON "iast_vul_overpower" ("agent_id");
CREATE INDEX "iast_vulnerability_agent_id_a029394b" ON "iast_vulnerability" ("agent_id");
CREATE INDEX "iast_vulnerability_level_id_6382d09e" ON "iast_vulnerability" ("level_id");
CREATE INDEX "iast_system_user_id_c83e80ce" ON "iast_system" ("user_id");
CREATE INDEX "iast_strategy_user_user_id_0bddb2a4" ON "iast_strategy_user" ("user_id");
CREATE INDEX "iast_strategy_hook_type_id_8dee9a71" ON "iast_strategy" ("hook_type_id");
CREATE INDEX "iast_strategy_level_id_d5ed00d0" ON "iast_strategy" ("level_id");
CREATE INDEX "iast_strategy_user_id_4530fb9f" ON "iast_strategy" ("user_id");
CREATE INDEX "iast_replay_queue_agent_id_1c4714cf" ON "iast_replay_queue" ("agent_id");
CREATE INDEX "iast_project_version_project_id_0a63e2be" ON "iast_project_version" ("project_id");
CREATE INDEX "iast_project_version_user_id_d52e8faf" ON "iast_project_version" ("user_id");
CREATE INDEX "iast_project_scan_id_08eb0b8f" ON "iast_project" ("scan_id");
--
-- Add field user to iastproject
--
CREATE TABLE "new__iast_project" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(255) NULL, "mode" varchar(255) NULL, "vul_count" integer unsigned NULL CHECK ("vul_count" >= 0), "agent_count" integer NULL, "latest_time" integer NULL, "scan_id" bigint NULL REFERENCES "iast_strategy_user" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__iast_project" ("id", "name", "mode", "vul_count", "agent_count", "latest_time", "scan_id", "user_id") SELECT "id", "name", "mode", "vul_count", "agent_count", "latest_time", "scan_id", NULL FROM "iast_project";
DROP TABLE "iast_project";
ALTER TABLE "new__iast_project" RENAME TO "iast_project";
CREATE INDEX "iast_project_scan_id_08eb0b8f" ON "iast_project" ("scan_id");
CREATE INDEX "iast_project_user_id_c863b2cf" ON "iast_project" ("user_id");
--
-- Create model IastHeartbeat
--
CREATE TABLE "iast_heartbeat" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "memory" varchar(1000) NULL, "cpu" varchar(1000) NULL, "disk" varchar(1000) NULL, "req_count" integer NULL, "dt" integer NULL, "agent_id" integer NULL REFERENCES "iast_agent" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model IastErrorlog
--
CREATE TABLE "iast_errorlog" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "errorlog" text NULL, "state" varchar(50) NULL, "dt" integer NULL, "agent_id" integer NULL REFERENCES "iast_agent" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model IastAgentMethodPoolReplay
--
CREATE TABLE "iast_agent_method_pool_replay" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "url" varchar(2000) NULL, "uri" varchar(2000) NULL, "http_method" varchar(10) NULL, "http_scheme" varchar(20) NULL, "http_protocol" varchar(255) NULL, "req_header" varchar(2000) NULL, "req_params" varchar(2000) NULL, "req_data" varchar(4000) NULL, "res_header" varchar(1000) NULL, "res_body" varchar(1000) NULL, "context_path" varchar(255) NULL, "method_pool" text NULL, "clent_ip" varchar(255) NULL, "create_time" integer NULL, "update_time" integer NULL, "replay_id" integer NULL, "replay_type" integer NULL, "relation_id" integer NULL, "agent_id" integer NULL REFERENCES "iast_agent" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Add field server to iastagent
--
CREATE TABLE "new__iast_agent" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "token" varchar(255) NULL, "version" varchar(255) NULL, "latest_time" integer NULL, "is_running" integer NULL, "is_core_running" integer NULL, "control" integer NULL, "is_control" integer NULL, "bind_project_id" integer NULL, "project_name" varchar(255) NULL, "online" smallint unsigned NOT NULL CHECK ("online" >= 0), "project_version_id" integer NULL, "language" varchar(10) NULL, "server_id" integer NOT NULL REFERENCES "iast_server" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__iast_agent" ("id", "token", "version", "latest_time", "is_running", "is_core_running", "control", "is_control", "bind_project_id", "project_name", "online", "project_version_id", "language", "server_id") SELECT "id", "token", "version", "latest_time", "is_running", "is_core_running", "control", "is_control", "bind_project_id", "project_name", "online", "project_version_id", "language", NULL FROM "iast_agent";
DROP TABLE "iast_agent";
ALTER TABLE "new__iast_agent" RENAME TO "iast_agent";
CREATE INDEX "iast_heartbeat_agent_id_a1d28300" ON "iast_heartbeat" ("agent_id");
CREATE INDEX "iast_errorlog_agent_id_1a8a0ccb" ON "iast_errorlog" ("agent_id");
CREATE INDEX "iast_agent_method_pool_replay_agent_id_9799408c" ON "iast_agent_method_pool_replay" ("agent_id");
CREATE INDEX "iast_agent_server_id_18c797f1" ON "iast_agent" ("server_id");
--
-- Add field user to iastagent
--
CREATE TABLE "new__iast_agent" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "token" varchar(255) NULL, "version" varchar(255) NULL, "latest_time" integer NULL, "is_running" integer NULL, "is_core_running" integer NULL, "control" integer NULL, "is_control" integer NULL, "bind_project_id" integer NULL, "project_name" varchar(255) NULL, "online" smallint unsigned NOT NULL CHECK ("online" >= 0), "project_version_id" integer NULL, "language" varchar(10) NULL, "server_id" integer NOT NULL REFERENCES "iast_server" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__iast_agent" ("id", "token", "version", "latest_time", "is_running", "is_core_running", "control", "is_control", "bind_project_id", "project_name", "online", "project_version_id", "language", "server_id", "user_id") SELECT "id", "token", "version", "latest_time", "is_running", "is_core_running", "control", "is_control", "bind_project_id", "project_name", "online", "project_version_id", "language", "server_id", NULL FROM "iast_agent";
DROP TABLE "iast_agent";
ALTER TABLE "new__iast_agent" RENAME TO "iast_agent";
CREATE INDEX "iast_agent_server_id_18c797f1" ON "iast_agent" ("server_id");
CREATE INDEX "iast_agent_user_id_d54d85ea" ON "iast_agent" ("user_id");
--
-- Add field type to hookstrategy
--
CREATE TABLE "iast_hook_strategy_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "hookstrategy_id" integer NOT NULL REFERENCES "iast_hook_strategy" ("id") DEFERRABLE INITIALLY DEFERRED, "hooktype_id" integer NOT NULL REFERENCES "iast_hook_type" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Department
--
CREATE TABLE "auth_department" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL UNIQUE, "create_time" integer NOT NULL, "update_time" integer NOT NULL, "created_by" integer NOT NULL, "parent_id" integer NOT NULL);
CREATE TABLE "auth_department_talent" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "department_id" integer NOT NULL REFERENCES "auth_department" ("id") DEFERRABLE INITIALLY DEFERRED, "talent_id" integer NOT NULL REFERENCES "auth_talent" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Asset
--
CREATE TABLE "iast_asset" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "package_name" varchar(255) NULL, "package_path" varchar(255) NULL, "signature_algorithm" varchar(255) NULL, "signature_value" varchar(255) NULL, "dt" integer NULL, "version" varchar(255) NULL, "vul_count" integer NULL, "agent_id" integer NULL REFERENCES "iast_agent" ("id") DEFERRABLE INITIALLY DEFERRED, "level_id" integer NULL REFERENCES "iast_vul_level" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Add field department to user
--
CREATE TABLE "auth_user_department" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "department_id" integer NOT NULL REFERENCES "auth_department" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Add field groups to user
--
CREATE TABLE "auth_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Add field user_permissions to user
--
CREATE TABLE "auth_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model ScaMavenArtifact
--
CREATE TABLE "sca_maven_artifact" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "safe_version" varchar(255) NULL, "version_range" varchar(255) NULL, "cph_version" varchar(255) NULL, "dt" integer NULL, "patch" varchar(255) NULL, "cph" varchar(255) NULL, "type" varchar(255) NULL, "group_id" varchar(255) NULL, "artifact_id" varchar(255) NULL, "version" varchar(255) NULL, "signature" varchar(255) NULL, "package_name" varchar(255) NULL, "aid" integer NULL REFERENCES "sca_artifact_db" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "iast_hook_strategy_type_hookstrategy_id_hooktype_id_87f7fb37_uniq" ON "iast_hook_strategy_type" ("hookstrategy_id", "hooktype_id");
CREATE INDEX "iast_hook_strategy_type_hookstrategy_id_0cac1cb8" ON "iast_hook_strategy_type" ("hookstrategy_id");
CREATE INDEX "iast_hook_strategy_type_hooktype_id_21d98ea3" ON "iast_hook_strategy_type" ("hooktype_id");
CREATE UNIQUE INDEX "auth_department_talent_department_id_talent_id_9c5185ea_uniq" ON "auth_department_talent" ("department_id", "talent_id");
CREATE INDEX "auth_department_talent_department_id_e0a8f05d" ON "auth_department_talent" ("department_id");
CREATE INDEX "auth_department_talent_talent_id_3ea31765" ON "auth_department_talent" ("talent_id");
CREATE INDEX "iast_asset_agent_id_effa4b6e" ON "iast_asset" ("agent_id");
CREATE INDEX "iast_asset_level_id_7e3c377d" ON "iast_asset" ("level_id");
CREATE UNIQUE INDEX "auth_user_department_user_id_department_id_f26be25b_uniq" ON "auth_user_department" ("user_id", "department_id");
CREATE INDEX "auth_user_department_user_id_5b617c46" ON "auth_user_department" ("user_id");
CREATE INDEX "auth_user_department_department_id_9dc2f123" ON "auth_user_department" ("department_id");
CREATE UNIQUE INDEX "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" ("user_id", "group_id");
CREATE INDEX "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" ("user_id");
CREATE INDEX "auth_user_groups_group_id_97559544" ON "auth_user_groups" ("group_id");
CREATE UNIQUE INDEX "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" ("user_id", "permission_id");
CREATE INDEX "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" ("user_id");
CREATE INDEX "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" ("permission_id");
CREATE UNIQUE INDEX "sca_maven_artifact_cph_version_aid_35f13689_uniq" ON "sca_maven_artifact" ("cph_version", "aid");
CREATE INDEX "sca_maven_artifact_aid_cbbb8971" ON "sca_maven_artifact" ("aid");
COMMIT;
