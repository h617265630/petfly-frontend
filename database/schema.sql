-- =====================================================
-- PET FLY 数据库 Schema (重新设计)
-- 宠物陪飞匹配平台
-- 
-- 业务流程：
-- 1. 主人发布任务 → 2. 培飞员申请 → 3. 主人选择 → 4. 管理员确认
-- =====================================================

-- -----------------------------------------------------
-- 1. 用户表
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `users` (
  `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `phone` VARCHAR(20) NOT NULL COMMENT '手机号',
  `country_code` VARCHAR(10) DEFAULT '+86' COMMENT '国家区号',
  `wechat` VARCHAR(100) COMMENT '微信号',
  `role` ENUM('OWNER', 'FLYER', 'MANAGER') NOT NULL DEFAULT 'OWNER' COMMENT '角色: 主人/培飞员/管理员',
  `name` VARCHAR(100) COMMENT '姓名',
  `avatar` VARCHAR(500) COMMENT '头像URL',
  `status` TINYINT DEFAULT 1 COMMENT '状态: 0禁用, 1正常',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `idx_phone` (`phone`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- -----------------------------------------------------
-- 2. 培飞员详细信息表
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `flyer_profiles` (
  `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `user_id` BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
  
  -- 护照信息
  `passport_name` VARCHAR(100) COMMENT '护照姓名',
  `passport_number` VARCHAR(50) COMMENT '护照号码',
  `passport_expiry` DATE COMMENT '护照有效期',
  `passport_image` VARCHAR(500) COMMENT '护照图片',
  
  -- 签证信息
  `visa_type` ENUM('Tourist', 'Work', 'Student', 'Other') COMMENT '签证类型',
  `visa_expiry` DATE COMMENT '签证有效期',
  `visa_image` VARCHAR(500) COMMENT '签证图片',
  
  -- 养宠经验
  `has_pet_experience` TINYINT DEFAULT 0 COMMENT '是否有养宠经验',
  `pet_experience_desc` TEXT COMMENT '养宠经验描述',
  `pet_types_handled` VARCHAR(200) COMMENT '处理过的宠物类型',
  
  -- 认证状态
  `is_verified` TINYINT DEFAULT 0 COMMENT '是否认证: 0未认证, 1已认证',
  `verified_at` TIMESTAMP NULL COMMENT '认证时间',
  
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  UNIQUE KEY `idx_user_id` (`user_id`),
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='培飞员详细信息表';

-- -----------------------------------------------------
-- 3. 宠物表
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pets` (
  `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `owner_id` BIGINT UNSIGNED NOT NULL COMMENT '主人ID',
  `name` VARCHAR(100) COMMENT '宠物名字',
  `type` ENUM('DOG', 'CAT', 'OTHER') NOT NULL COMMENT '宠物类型',
  `breed` VARCHAR(200) COMMENT '品种',
  `weight` DECIMAL(5,2) COMMENT '体重(kg)',
  `age_months` INT COMMENT '年龄(月)',
  `gender` ENUM('Male', 'Female') COMMENT '性别',
  `image` VARCHAR(500) COMMENT '宠物图片',
  `vaccination_record` VARCHAR(500) COMMENT '疫苗记录',
  `health_cert` VARCHAR(500) COMMENT '健康证明',
  `remark` TEXT COMMENT '备注',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  KEY `idx_owner_id` (`owner_id`),
  FOREIGN KEY (`owner_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='宠物表';

-- -----------------------------------------------------
-- 4. 任务表 (主人发布)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tasks` (
  `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `owner_id` BIGINT UNSIGNED NOT NULL COMMENT '发布主人ID',
  `pet_id` BIGINT UNSIGNED COMMENT '关联宠物ID',
  
  -- 运输信息
  `transport_type` ENUM('CABIN', 'CARGO', 'BOTH') DEFAULT 'CABIN' COMMENT '运输类型: 随机托运/货运/均可',
  `from_city` VARCHAR(100) NOT NULL COMMENT '出发城市',
  `to_city` VARCHAR(100) NOT NULL COMMENT '目的城市',
  `middle_city` VARCHAR(100) COMMENT '中转城市',
  
  -- 时间
  `travel_date` DATE NOT NULL COMMENT '出行日期',
  `deadline` DATETIME COMMENT '报名截止时间',
  
  -- 预算
  `budget_min` DECIMAL(10,2) COMMENT '预算下限(元)',
  `budget_max` DECIMAL(10,2) COMMENT '预算上限(元)',
  
  -- 状态流转
  `status` ENUM('DRAFT', 'PENDING', 'OPEN', 'SELECTING', 'CONFIRMING', 'CONFIRMED', 'COMPLETED', 'CANCELLED') DEFAULT 'DRAFT' COMMENT '任务状态',
  `selected_flyer_id` BIGINT UNSIGNED COMMENT '被选中的培飞员ID',
  `confirmed_at` TIMESTAMP NULL COMMENT '确认时间',
  
  `remark` TEXT COMMENT '备注',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  KEY `idx_owner_id` (`owner_id`),
  KEY `idx_status` (`status`),
  KEY `idx_from_to` (`from_city`, `to_city`),
  KEY `idx_travel_date` (`travel_date`),
  FOREIGN KEY (`owner_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='任务表';

-- 任务状态说明：
-- DRAFT      - 草稿
-- PENDING    - 待审核（管理员审核）
-- OPEN       - 开放报名（培飞员可申请）
-- SELECTING  - 选择中（主人选择培飞员）
-- CONFIRMING - 确认中（等待管理员确认）
-- CONFIRMED  - 已确认（匹配成功）
-- COMPLETED  - 已完成
-- CANCELLED  - 已取消

-- -----------------------------------------------------
-- 5. 申请记录表 (培飞员申请任务)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `task_applications` (
  `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `task_id` BIGINT UNSIGNED NOT NULL COMMENT '任务ID',
  `flyer_id` BIGINT UNSIGNED NOT NULL COMMENT '申请培飞员ID',
  
  -- 培飞员提供的行程信息
  `from_city` VARCHAR(100) COMMENT '出发城市',
  `to_city` VARCHAR(100) COMMENT '目的城市',
  `travel_date` DATE COMMENT '出行日期',
  `flight_number` VARCHAR(50) COMMENT '航班号',
  
  -- 自我介绍/申请理由
  `introduction` TEXT COMMENT '自我介绍',
  `can_handle_pet_type` VARCHAR(200) COMMENT '能处理的宠物类型',
  `has_experience` TINYINT DEFAULT 0 COMMENT '是否有经验',
  `experience_desc` TEXT COMMENT '经验描述',
  
  -- 期望报酬
  `expected_price` DECIMAL(10,2) COMMENT '期望报酬(元)',
  
  -- 状态
  `status` ENUM('PENDING', 'SHORTLISTED', 'ACCEPTED', 'REJECTED', 'WITHDRAWN') DEFAULT 'PENDING' COMMENT '申请状态',
  `reject_reason` VARCHAR(500) COMMENT '拒绝原因',
  
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  UNIQUE KEY `idx_task_flyer` (`task_id`, `flyer_id`),
  KEY `idx_task_id` (`task_id`),
  KEY `idx_flyer_id` (`flyer_id`),
  KEY `idx_status` (`status`),
  FOREIGN KEY (`task_id`) REFERENCES `tasks`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`flyer_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='申请记录表';

-- 申请状态说明：
-- PENDING     - 待审核
-- SHORTLISTED - 入围（主人选中）
-- ACCEPTED    - 已接受
-- REJECTED    - 已拒绝
-- WITHDRAWN   - 已撤回

-- -----------------------------------------------------
-- 6. 管理员审核记录表
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `task_confirmations` (
  `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `task_id` BIGINT UNSIGNED NOT NULL COMMENT '任务ID',
  `flyer_id` BIGINT UNSIGNED NOT NULL COMMENT '被确认的培飞员ID',
  
  -- 审核信息
  `manager_id` BIGINT UNSIGNED COMMENT '审核管理员ID',
  `status` ENUM('PENDING', 'APPROVED', 'REJECTED') DEFAULT 'PENDING' COMMENT '审核状态',
  `remark` VARCHAR(500) COMMENT '审核备注',
  `reject_reason` VARCHAR(500) COMMENT '拒绝原因',
  
  -- 审核时间
  `reviewed_at` TIMESTAMP NULL COMMENT '审核时间',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  UNIQUE KEY `idx_task_id` (`task_id`),
  FOREIGN KEY (`task_id`) REFERENCES `tasks`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`flyer_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`manager_id`) REFERENCES `users`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='管理员审核记录表';

-- -----------------------------------------------------
-- 7. 消息通知表
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `notifications` (
  `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `user_id` BIGINT UNSIGNED NOT NULL COMMENT '接收者ID',
  `type` ENUM(
    'TASK_NEW',           -- 新任务发布
    'TASK_OPEN',          -- 任务开放
    'APPLICATION_NEW',    -- 新申请
    'APPLICATION_ACCEPTED', -- 申请被接受
    'APPLICATION_REJECTED', -- 申请被拒绝
    'SELECTED',           -- 被主人选中
    'CONFIRM_REQUEST',    -- 待确认
    'CONFIRMED',          -- 已确认
    'CONFIRM_REJECTED',  -- 确认被拒绝
    'SYSTEM'
  ) NOT NULL COMMENT '通知类型',
  
  `title` VARCHAR(200) NOT NULL COMMENT '标题',
  `content` TEXT COMMENT '内容',
  
  -- 关联信息
  `related_id` BIGINT UNSIGNED COMMENT '关联ID',
  `related_type` VARCHAR(50) COMMENT '关联类型: task/application',
  
  `is_read` TINYINT DEFAULT 0 COMMENT '是否已读: 0未读, 1已读',
  `read_at` TIMESTAMP NULL COMMENT '阅读时间',
  
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  KEY `idx_user_id` (`user_id`),
  KEY `idx_type` (`type`),
  KEY `idx_is_read` (`is_read`),
  KEY `idx_created_at` (`created_at`),
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='消息通知表';

-- -----------------------------------------------------
-- 8. 聊天会话表
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `conversations` (
  `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `task_id` BIGINT UNSIGNED COMMENT '关联任务ID',
  `owner_id` BIGINT UNSIGNED NOT NULL COMMENT '主人ID',
  `flyer_id` BIGINT UNSIGNED NOT NULL COMMENT '培飞员ID',
  
  `last_message` VARCHAR(500) COMMENT '最后一条消息',
  `last_message_at` TIMESTAMP NULL COMMENT '最后消息时间',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  UNIQUE KEY `idx_task_id` (`task_id`),
  KEY `idx_owner_id` (`owner_id`),
  KEY `idx_flyer_id` (`flyer_id`),
  FOREIGN KEY (`owner_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`flyer_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='聊天会话表';

-- -----------------------------------------------------
-- 9. 聊天消息表
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `messages` (
  `id` BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `conversation_id` BIGINT UNSIGNED NOT NULL COMMENT '会话ID',
  `sender_id` BIGINT UNSIGNED NOT NULL COMMENT '发送者ID',
  
  `content` TEXT NOT NULL COMMENT '消息内容',
  `type` ENUM('TEXT', 'IMAGE', 'FILE') DEFAULT 'TEXT' COMMENT '消息类型',
  `is_read` TINYINT DEFAULT 0 COMMENT '是否已读',
  
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  KEY `idx_conversation_id` (`conversation_id`),
  KEY `idx_sender_id` (`sender_id`),
  FOREIGN KEY (`conversation_id`) REFERENCES `conversations`(`id`) ON DELETE CASCADE,
  FOREIGN KEY (`sender_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='聊天消息表';

-- =====================================================
-- 索引汇总
-- =====================================================

-- tasks 表索引
-- ALTER TABLE `tasks` ADD INDEX `idx_travel_date` (`travel_date`);
-- ALTER TABLE `tasks` ADD INDEX `idx_status_date` (`status`, `travel_date`);

-- task_applications 表索引
-- ALTER TABLE `task_applications` ADD INDEX `idx_task_status` (`task_id`, `status`);

-- notifications 表索引
-- ALTER TABLE `notifications` ADD INDEX `idx_user_read` (`user_id`, `is_read`);
