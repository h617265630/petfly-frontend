const jsonServer = require('json-server')
const server = jsonServer.create()
const router = jsonServer.router('db.json')
const middlewares = jsonServer.defaults

const PORT = 3001

// 设置 CORS 头
server.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*')
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization')
  
  if (req.method === 'OPTIONS') {
    return res.sendStatus(200)
  }
  next()
})

server.use(middlewares())
server.use(router)

server.listen(PORT, () => {
  console.log(`✅ PetFly Mock API Server running at http://localhost:${PORT}`)
  console.log(`📋 Available endpoints:`)
  console.log(`   - GET    /users`)
  console.log(`   - GET    /tasks`)
  console.log(`   - GET    /tasks/open`)
  console.log(`   - GET    /task_applications?task_id=1`)
  console.log(`   - GET    /notifications?user_id=1`)
  console.log(`   - POST   /tasks`)
  console.log(`   - POST   /task_applications`)
})
