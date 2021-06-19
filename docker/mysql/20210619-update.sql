SET FOREIGN_KEY_CHECKS=0;

ALTER TABLE `iast_agent` ADD COLUMN `project_version_id` int(11) NULL DEFAULT 0 COMMENT '项目版本ID' AFTER `project_name`;

ALTER TABLE `iast_agent` ADD COLUMN `online` tinyint(4) NULL DEFAULT 0 COMMENT '1在线运行，0未运行，同token，仅一个online' AFTER `project_version_id`;

ALTER TABLE `iast_agent` ADD COLUMN `is_core_running` int(11) NULL DEFAULT NULL COMMENT '核心引擎是否启动' AFTER `online`;

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

SET FOREIGN_KEY_CHECKS=1;
