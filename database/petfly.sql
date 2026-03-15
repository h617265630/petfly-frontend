-- =====================================================
-- PetFly 数据库 Schema (PostgreSQL)
-- =====================================================

-- 用户表
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  phone VARCHAR(20) UNIQUE,
  country_code VARCHAR(10) DEFAULT '+86',
  wechat VARCHAR(100),
  role VARCHAR(20) DEFAULT 'OWNER',
  name VARCHAR(100),
  avatar VARCHAR(500),
  status INT DEFAULT 1,
  username VARCHAR(100),
  password VARCHAR(100),
  gender VARCHAR(20),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- 培飞员资料表
CREATE TABLE IF NOT EXISTS flyer_profiles (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL UNIQUE,
  passport_name VARCHAR(100),
  passport_number VARCHAR(50),
  passport_expiry DATE,
  visa_type VARCHAR(20),
  visa_expiry DATE,
  has_pet_experience INT DEFAULT 0,
  pet_experience_desc TEXT,
  pet_types_handled VARCHAR(200),
  is_verified INT DEFAULT 0,
  verified_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- 宠物表
CREATE TABLE IF NOT EXISTS pets (
  id SERIAL PRIMARY KEY,
  owner_id INT NOT NULL,
  name VARCHAR(100),
  type VARCHAR(20) NOT NULL,
  breed VARCHAR(200),
  weight DECIMAL(5,2),
  age_months INT,
  gender VARCHAR(20),
  image VARCHAR(500),
  vaccination_record VARCHAR(500),
  health_cert VARCHAR(500),
  remark TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- 任务表
CREATE TABLE IF NOT EXISTS tasks (
  id SERIAL PRIMARY KEY,
  owner_id INT NOT NULL,
  pet_id INT,
  transport_type VARCHAR(20) DEFAULT 'CABIN',
  from_city VARCHAR(100) NOT NULL,
  to_city VARCHAR(100) NOT NULL,
  middle_city VARCHAR(100),
  travel_date DATE NOT NULL,
  deadline TIMESTAMP,
  budget_min DECIMAL(10,2),
  budget_max DECIMAL(10,2),
  status VARCHAR(20) DEFAULT 'OPEN',
  selected_flyer_id INT,
  confirmed_at TIMESTAMP,
  remark TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- 申请表
CREATE TABLE IF NOT EXISTS task_applications (
  id SERIAL PRIMARY KEY,
  task_id INT NOT NULL,
  flyer_id INT NOT NULL,
  from_city VARCHAR(100),
  to_city VARCHAR(100),
  travel_date DATE,
  flight_number VARCHAR(50),
  introduction TEXT,
  can_handle_pet_type VARCHAR(200),
  has_experience INT DEFAULT 0,
  experience_desc TEXT,
  expected_price DECIMAL(10,2),
  status VARCHAR(20) DEFAULT 'PENDING',
  reject_reason VARCHAR(500),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(task_id, flyer_id)
);

-- 通知表
CREATE TABLE IF NOT EXISTS notifications (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL,
  type VARCHAR(50) NOT NULL,
  title VARCHAR(200) NOT NULL,
  content TEXT,
  related_id INT,
  related_type VARCHAR(50),
  is_read INT DEFAULT 0,
  read_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

-- 任务确认表
CREATE TABLE IF NOT EXISTS task_confirmations (
  id SERIAL PRIMARY KEY,
  task_id INT NOT NULL,
  flyer_id INT NOT NULL,
  manager_id INT,
  status VARCHAR(20) DEFAULT 'PENDING',
  remark VARCHAR(500),
  reviewed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);
