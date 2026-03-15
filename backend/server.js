require('dotenv').config();
const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// 简单的健康检查
app.get('/', (req, res) => {
  res.json({ status: 'ok', message: 'PetFly API is running' });
});

app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

// 导入路由
const pool = require('./db');

// ==================== 用户 API ====================

// 获取所有用户
app.get('/users', async (req, res) => {
  try {
    const { role } = req.query;
    let query = 'SELECT * FROM users';
    const params = [];
    
    if (role) {
      query += ' WHERE role = $1';
      params.push(role);
    }
    
    query += ' ORDER BY id DESC';
    const result = await pool.query(query, params);
    res.json(result.rows);
  } catch (err) {
    console.error('Error:', err.message);
    res.status(500).json({ error: err.message });
  }
});

// 获取单个用户
app.get('/users/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 用户注册
app.post('/users', async (req, res) => {
  try {
    const { phone, country_code, wechat, role, name, avatar, status, gender, username, password } = req.body;
    
    const checkResult = await pool.query('SELECT id FROM users WHERE phone = $1', [phone]);
    if (checkResult.rows.length > 0) {
      return res.status(400).json({ error: '手机号已注册' });
    }
    
    const result = await pool.query(
      `INSERT INTO users (phone, country_code, wechat, role, name, avatar, status, gender, username, password)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) RETURNING *`,
      [phone, country_code || '+86', wechat, role || 'OWNER', name, avatar, status || 1, gender, username, password]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 用户登录
app.post('/users/login', async (req, res) => {
  try {
    const { phone, password } = req.body;
    const result = await pool.query('SELECT * FROM users WHERE phone = $1', [phone]);
    
    if (result.rows.length === 0) {
      return res.status(401).json({ error: '用户不存在' });
    }
    
    const user = result.rows[0];
    if (user.password !== password) {
      return res.status(401).json({ error: '密码错误' });
    }
    
    res.json(user);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ==================== 宠物 API ====================

app.get('/pets', async (req, res) => {
  try {
    const { owner_id } = req.query;
    let query = 'SELECT * FROM pets';
    const params = [];
    
    if (owner_id) {
      query += ' WHERE owner_id = $1';
      params.push(owner_id);
    }
    
    query += ' ORDER BY id DESC';
    const result = await pool.query(query, params);
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/pets', async (req, res) => {
  try {
    const { owner_id, name, type, breed, weight, age_months, gender, image, vaccination_record, health_cert, remark } = req.body;
    const result = await pool.query(
      `INSERT INTO pets (owner_id, name, type, breed, weight, age_months, gender, image, vaccination_record, health_cert, remark)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11) RETURNING *`,
      [owner_id, name, type, breed, weight, age_months, gender, image, vaccination_record, health_cert, remark]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ==================== 任务 API ====================

app.get('/tasks', async (req, res) => {
  try {
    const { status, owner_id } = req.query;
    let query = 'SELECT * FROM tasks';
    const conditions = [];
    const params = [];
    let paramIndex = 1;
    
    if (status) {
      conditions.push(`status = $${paramIndex++}`);
      params.push(status);
    }
    if (owner_id) {
      conditions.push(`owner_id = $${paramIndex++}`);
      params.push(owner_id);
    }
    
    if (conditions.length > 0) {
      query += ' WHERE ' + conditions.join(' AND ');
    }
    
    query += ' ORDER BY id DESC';
    const result = await pool.query(query, params);
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/tasks/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const result = await pool.query('SELECT * FROM tasks WHERE id = $1', [id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Task not found' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/tasks', async (req, res) => {
  try {
    const { owner_id, pet_id, transport_type, from_city, to_city, middle_city, travel_date, deadline, budget_min, budget_max, remark } = req.body;
    const result = await pool.query(
      `INSERT INTO tasks (owner_id, pet_id, transport_type, from_city, to_city, middle_city, travel_date, deadline, budget_min, budget_max, status, remark)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, 'OPEN', $11) RETURNING *`,
      [owner_id, pet_id, transport_type, from_city, to_city, middle_city, travel_date, deadline, budget_min, budget_max, remark]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.patch('/tasks/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const updates = req.body;
    const fields = Object.keys(updates);
    const values = Object.values(updates);
    
    if (fields.length === 0) {
      return res.status(400).json({ error: 'No fields to update' });
    }
    
    const setClause = fields.map((field, index) => `${field} = $${index + 1}`).join(', ');
    const query = `UPDATE tasks SET ${setClause} WHERE id = $${fields.length + 1} RETURNING *`;
    
    const result = await pool.query(query, [...values, id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Task not found' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ==================== 申请 API ====================

app.get('/task_applications', async (req, res) => {
  try {
    const { task_id, flyer_id, status } = req.query;
    let query = 'SELECT * FROM task_applications';
    const conditions = [];
    const params = [];
    let paramIndex = 1;
    
    if (task_id) {
      conditions.push(`task_id = $${paramIndex++}`);
      params.push(task_id);
    }
    if (flyer_id) {
      conditions.push(`flyer_id = $${paramIndex++}`);
      params.push(flyer_id);
    }
    if (status) {
      conditions.push(`status = $${paramIndex++}`);
      params.push(status);
    }
    
    if (conditions.length > 0) {
      query += ' WHERE ' + conditions.join(' AND ');
    }
    
    query += ' ORDER BY id DESC';
    const result = await pool.query(query, params);
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/task_applications', async (req, res) => {
  try {
    const { task_id, flyer_id, from_city, to_city, travel_date, flight_number, introduction, can_handle_pet_type, has_experience, experience_desc, expected_price } = req.body;
    
    const checkResult = await pool.query(
      'SELECT id FROM task_applications WHERE task_id = $1 AND flyer_id = $2',
      [task_id, flyer_id]
    );
    if (checkResult.rows.length > 0) {
      return res.status(400).json({ error: '已申请过该任务' });
    }
    
    const result = await pool.query(
      `INSERT INTO task_applications (task_id, flyer_id, from_city, to_city, travel_date, flight_number, introduction, can_handle_pet_type, has_experience, experience_desc, expected_price, status)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, 'PENDING') RETURNING *`,
      [task_id, flyer_id, from_city, to_city, travel_date, flight_number, introduction, can_handle_pet_type, has_experience, experience_desc, expected_price]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.patch('/task_applications/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const updates = req.body;
    const fields = Object.keys(updates);
    const values = Object.values(updates);
    
    if (fields.length === 0) {
      return res.status(400).json({ error: 'No fields to update' });
    }
    
    const setClause = fields.map((field, index) => `${field} = $${index + 1}`).join(', ');
    const query = `UPDATE task_applications SET ${setClause} WHERE id = $${fields.length + 1} RETURNING *`;
    
    const result = await pool.query(query, [...values, id]);
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Application not found' });
    }
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ==================== 通知 API ====================

app.get('/notifications', async (req, res) => {
  try {
    const { user_id, is_read } = req.query;
    let query = 'SELECT * FROM notifications';
    const conditions = [];
    const params = [];
    let paramIndex = 1;
    
    if (user_id) {
      conditions.push(`user_id = $${paramIndex++}`);
      params.push(user_id);
    }
    if (is_read !== undefined) {
      conditions.push(`is_read = $${paramIndex++}`);
      params.push(is_read);
    }
    
    if (conditions.length > 0) {
      query += ' WHERE ' + conditions.join(' AND ');
    }
    
    query += ' ORDER BY id DESC';
    const result = await pool.query(query, params);
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/notifications', async (req, res) => {
  try {
    const { user_id, type, title, content, related_id, related_type } = req.body;
    const result = await pool.query(
      `INSERT INTO notifications (user_id, type, title, content, related_id, related_type, is_read)
       VALUES ($1, $2, $3, $4, $5, $6, 0) RETURNING *`,
      [user_id, type, title, content, related_id, related_type]
    );
    res.status(201).json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.patch('/notifications/:id/read', async (req, res) => {
  try {
    const { id } = req.params;
    const result = await pool.query(
      'UPDATE notifications SET is_read = 1, read_at = NOW() WHERE id = $1 RETURNING *',
      [id]
    );
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ==================== 培飞员资料 API ====================

app.get('/flyer_profiles', async (req, res) => {
  try {
    const { user_id } = req.query;
    let query = 'SELECT * FROM flyer_profiles';
    const params = [];
    
    if (user_id) {
      query += ' WHERE user_id = $1';
      params.push(user_id);
    }
    
    const result = await pool.query(query, params);
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/flyer_profiles', async (req, res) => {
  try {
    const { user_id, passport_name, passport_number, passport_expiry, visa_type, visa_expiry, has_pet_experience, pet_experience_desc, pet_types_handled } = req.body;
    
    const checkResult = await pool.query('SELECT id FROM flyer_profiles WHERE user_id = $1', [user_id]);
    
    let result;
    if (checkResult.rows.length > 0) {
      result = await pool.query(
        `UPDATE flyer_profiles SET passport_name = $1, passport_number = $2, passport_expiry = $3, visa_type = $4, visa_expiry = $5, has_pet_experience = $6, pet_experience_desc = $7, pet_types_handled = $8 WHERE user_id = $9 RETURNING *`,
        [passport_name, passport_number, passport_expiry, visa_type, visa_expiry, has_pet_experience, pet_experience_desc, pet_types_handled, user_id]
      );
    } else {
      result = await pool.query(
        `INSERT INTO flyer_profiles (user_id, passport_name, passport_number, passport_expiry, visa_type, visa_expiry, has_pet_experience, pet_experience_desc, pet_types_handled)
         VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING *`,
        [user_id, passport_name, passport_number, passport_expiry, visa_type, visa_expiry, has_pet_experience, pet_experience_desc, pet_types_handled]
      );
    }
    
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// 启动服务器
app.listen(PORT, '0.0.0.0', () => {
  console.log(`PetFly API server running on port ${PORT}`);
});
