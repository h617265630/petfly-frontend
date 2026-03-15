-- =====================================================
-- PetFly 测试数据 (PostgreSQL)
-- =====================================================

-- 插入用户数据
INSERT INTO users (id, phone, country_code, wechat, role, name, avatar, status, username, password, gender, created_at, updated_at) VALUES
(1, '13800138000', '+86', 'owner001', 'OWNER', '张三', NULL, 1, 'zhangsan', '123456', NULL, '2026-03-01 10:00:00'::timestamp, '2026-03-01 10:00:00'::timestamp),
(2, '13800138001', '+86', 'flyer001', 'FLYER', '李四', NULL, 1, 'lisi', '123456', NULL, '2026-03-01 10:00:00'::timestamp, '2026-03-01 10:00:00'::timestamp),
(3, '13800138002', '+86', 'flyer002', 'FLYER', '王五', NULL, 1, 'wangwu', '123456', NULL, '2026-03-01 10:00:00'::timestamp, '2026-03-01 10:00:00'::timestamp),
(4, '13800138003', '+86', 'admin001', 'MANAGER', '管理员', NULL, 1, 'admin', 'admin123', NULL, '2026-03-01 10:00:00'::timestamp, '2026-03-01 10:00:00'::timestamp),
(5, NULL, '+86', NULL, 'OWNER', 'test', NULL, 1, 'testuser', 'test123', NULL, NULL, NULL),
(6, NULL, '+86', NULL, 'OWNER', 'test2', NULL, 1, 'testuser2', 'test123', NULL, NULL, NULL),
(7, NULL, '+86', NULL, 'OWNER', 'newuser', NULL, 1, 'newuser', 'test123', NULL, NULL, NULL),
(8, NULL, '+86', NULL, 'OWNER', 'test999', NULL, 1, 'test999', 'test123', 'Male', NULL, NULL),
(9, NULL, '+86', NULL, 'OWNER', 'user01', NULL, 1, 'user01', 'h12345678', 'Male', NULL, NULL),
(10, NULL, '+86', NULL, 'OWNER', 'user01', NULL, 1, 'user01', 'h12345678', 'Male', NULL, NULL),
(11, NULL, '+86', NULL, 'OWNER', 'nanny01', NULL, 1, 'nanny01', 'h12345678', 'Male', NULL, NULL),
(12, NULL, '+86', NULL, 'FLYER', 'nanny02', NULL, 1, 'nanny02', 'h12345678', 'Male', NULL, NULL),
(13, NULL, '+86', NULL, 'MANAGER', '超级管理员', NULL, 1, 'admin0987654321', 'admin1234567890', NULL, NULL, NULL)
ON CONFLICT (id) DO NOTHING;

-- 插入培飞员资料
INSERT INTO flyer_profiles (id, user_id, passport_name, passport_number, passport_expiry, visa_type, visa_expiry, has_pet_experience, pet_experience_desc, pet_types_handled, is_verified, verified_at, created_at, updated_at) VALUES
(1, 2, '李四', 'E12345678', '2030-12-31'::date, 'Work', '2027-12-31'::date, 1, '养狗5年，曾经帮朋友带过宠物', 'DOG,CAT', 1, '2026-03-01 10:00:00'::timestamp, '2026-03-01 10:00:00'::timestamp, '2026-03-01 10:00:00'::timestamp),
(2, 3, '王五', 'E87654321', '2028-12-31'::date, 'Tourist', '2026-06-30'::date, 1, '养猫3年', 'CAT', 1, '2026-03-01 10:00:00'::timestamp, '2026-03-01 10:00:00'::timestamp, '2026-03-01 10:00:00'::timestamp)
ON CONFLICT (id) DO NOTHING;

-- 插入宠物数据
INSERT INTO pets (id, owner_id, name, type, breed, weight, age_months, gender, image, vaccination_record, health_cert, remark, created_at, updated_at) VALUES
(1, 1, '豆豆', 'DOG', '金毛', 25.5, 24, 'Male', NULL, '已完成', '健康', '性格温顺', '2026-03-01 10:00:00'::timestamp, '2026-03-01 10:00:00'::timestamp),
(2, 1, '咪咪', 'CAT', '英短', 4.2, 12, 'Female', NULL, '已完成', '健康', '很乖', '2026-03-01 10:00:00'::timestamp, '2026-03-01 10:00:00'::timestamp),
(3, 9, '小小猫', 'DOG', '金毛', 20.0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(4, 9, '嘻嘻', 'DOG', '短腿', 15.0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)
ON CONFLICT (id) DO NOTHING;

-- 插入任务数据
INSERT INTO tasks (id, owner_id, pet_id, transport_type, from_city, to_city, middle_city, travel_date, deadline, budget_min, budget_max, status, selected_flyer_id, confirmed_at, remark, created_at, updated_at) VALUES
(1, 1, 1, 'CABIN', '上海', '北京', NULL, '2026-04-01'::date, NULL, 1500.00, 2500.00, 'OPEN', NULL, NULL, '希望找有经验的培飞员', '2026-03-10 10:00:00'::timestamp, '2026-03-10 10:00:00'::timestamp),
(2, 1, 2, 'CABIN', '深圳', '杭州', NULL, '2026-04-05'::date, NULL, 1000.00, 2000.00, 'OPEN', NULL, NULL, '猫咪需要小心照顾', '2026-03-11 10:00:00'::timestamp, '2026-03-11 10:00:00'::timestamp),
(3, 1, 1, 'CABIN', '广州', '上海', NULL, '2026-03-20'::date, NULL, 1800.00, 2200.00, 'CONFIRMED', 2, NULL, '已选择培飞员', '2026-03-12 10:00:00'::timestamp, '2026-03-13 10:00:00'::timestamp),
(4, 9, 3, 'CABIN', '洛杉矶', '悉尼', NULL, '2026-03-15'::date, NULL, 5000.00, 5000.00, 'OPEN', NULL, NULL, '照顾好', NULL, NULL),
(5, 9, 4, 'CABIN', '巴黎', '北京', NULL, '2026-03-27'::date, NULL, 7880.00, 7880.00, 'CONFIRMED', 12, NULL, '它怕光', NULL, NULL)
ON CONFLICT (id) DO NOTHING;

-- 插入申请数据
INSERT INTO task_applications (id, task_id, flyer_id, from_city, to_city, travel_date, flight_number, introduction, can_handle_pet_type, has_experience, experience_desc, expected_price, status, reject_reason, created_at, updated_at) VALUES
(1, 1, 2, '上海', '北京', '2026-04-01'::date, 'CA1234', '修改后的自我介绍', 'DOG,CAT', 1, '养过金毛和英短', 2000.00, 'PENDING', NULL, '2026-03-10 12:00:00'::timestamp, NULL),
(2, 1, 3, '上海', '北京', '2026-04-01'::date, 'MU5678', '我在上海工作，经常出差，可以帮忙带宠物', 'DOG', 1, '养狗3年', 1800.00, 'PENDING', NULL, '2026-03-10 14:00:00'::timestamp, NULL),
(3, 3, 2, '广州', '上海', '2026-03-20'::date, 'CZ9999', '我刚好有这趟航班，可以带宠物', 'DOG,CAT', 1, '专业培飞员', 2000.00, 'SHORTLISTED', NULL, '2026-03-12 12:00:00'::timestamp, NULL),
(4, 2, 12, '深圳', '杭州', '2026-04-05'::date, 'ca1234', '我是个好nanny', NULL, NULL, NULL, 2000.00, 'PENDING', NULL, NULL, NULL),
(5, 4, 12, '洛杉矶', '悉尼', '2026-03-15'::date, 'ca1234', '我经验很丰富', NULL, NULL, NULL, 7000.00, 'SHORTLISTED', NULL, NULL, NULL),
(6, 5, 12, '巴黎', '北京', '2026-03-27'::date, 'ca34567', '会斤斤计较', NULL, NULL, NULL, 7900.00, 'SHORTLISTED', NULL, NULL, NULL)
ON CONFLICT (id) DO NOTHING;

-- 插入通知数据
INSERT INTO notifications (id, user_id, type, title, content, related_id, related_type, is_read, read_at, created_at) VALUES
(1, 1, 'APPLICATION_NEW', '有新申请', '培飞员李四申请了您的任务', 1, 'application', 1, NULL, '2026-03-10 12:00:00'::timestamp),
(2, 1, 'APPLICATION_NEW', '有新申请', '培飞员王五申请了您的任务', 2, 'application', 1, NULL, '2026-03-10 14:00:00'::timestamp),
(3, 2, 'SELECTED', '您被选中了！', '任务 #3 的主人选择了您', 3, 'task', 0, NULL, '2026-03-13 10:00:00'::timestamp)
ON CONFLICT (id) DO NOTHING;
