import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'

// 配置 API 基础地址（支持环境变量）
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:3001'

// 创建 axios 实例
const api = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: false
})

// 添加响应拦截器处理错误
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error)
    if (error.code === 'ERR_NETWORK' || error.message === 'Network Error') {
      alert('网络错误，请确保后端服务正在运行 (localhost:3001)')
    }
    return Promise.reject(error)
  }
)

// 导出 api 供其他地方使用
export { api }

// ============ 用户相关 API ============
export const userApi = {
  getAll: () => api.get('/users').then(res => res.data),
  login: (phone: string) => api.get(`/users?phone=${phone}`).then(res => res.data[0]),
  loginByUsername: (username: string, password: string) => 
    api.get(`/users?username=${username}&password=${password}`).then(res => res.data[0]),
  checkUsername: (username: string) => 
    api.get(`/users?username=${username}`).then(res => res.data[0] || null),
  register: (data: any) => api.post('/users', data).then(res => res.data),
  getById: (id: number) => api.get(`/users/${id}`).then(res => res.data),
  update: (id: number, data: any) => api.patch(`/users/${id}`, data).then(res => res.data),
  getFlyerProfile: (userId: number) => api.get(`/flyer_profiles?user_id=${userId}`).then(res => res.data[0]),
  createFlyerProfile: (data: any) => api.post('/flyer_profiles', data).then(res => res.data),
}

// ============ 任务相关 API ============
export const taskApi = {
  getAll: (params?: any) => api.get('/tasks', { params }).then(res => res.data),
  getOpen: () => api.get('/tasks?status=OPEN').then(res => res.data),
  getMy: (ownerId: number) => api.get(`/tasks?owner_id=${ownerId}`).then(res => res.data),
  getById: (id: number) => api.get(`/tasks/${id}`).then(res => res.data),
  create: (data: any) => api.post('/tasks', data).then(res => res.data),
  update: (id: number, data: any) => api.patch(`/tasks/${id}`, data).then(res => res.data),
  delete: (id: number) => api.delete(`/tasks/${id}`).then(res => res.data),
  selectFlyer: (taskId: number, flyerId: number) => 
    api.patch(`/tasks/${taskId}`, { status: 'SELECTING', selected_flyer_id: flyerId }).then(res => res.data),
}

// ============ 申请相关 API ============
export const applicationApi = {
  getAll: () => api.get('/task_applications').then(res => res.data),
  getByTask: (taskId: number) => api.get(`/task_applications?task_id=${taskId}`).then(res => res.data),
  getApplicationById: (id: number) => api.get(`/task_applications/${id}`).then(res => res.data),
  getMy: (flyerId: number) => api.get(`/task_applications?flyer_id=${flyerId}`).then(res => res.data),
  create: (data: any) => api.post('/task_applications', data).then(res => res.data),
  update: (id: number, data: any) => api.patch(`/task_applications/${id}`, data).then(res => res.data),
  updateStatus: (id: number, status: string) => api.patch(`/task_applications/${id}`, { status }).then(res => res.data),
  delete: (id: number) => api.delete(`/task_applications/${id}`).then(res => res.data),
}

// ============ 通知相关 API ============
export const notificationApi = {
  getByUser: (userId: number) => api.get(`/notifications?user_id=${userId}&_sort=created_at&_order=desc`).then(res => res.data),
  getUnreadCount: (userId: number) => api.get(`/notifications?user_id=${userId}&is_read=0`).then(res => ({ count: res.data.length })),
  markAsRead: (id: number) => api.patch(`/notifications/${id}`, { is_read: 1 }).then(res => res.data),
  markAllAsRead: (userId: number) => 
    api.get(`/notifications?user_id=${userId}&is_read=0`).then(res => {
      const unread = res.data
      return Promise.all(unread.map((n: any) => api.patch(`/notifications/${n.id}`, { is_read: 1 })))
    }),
}

// ============ 宠物相关 API ============
export const petApi = {
  getMy: (ownerId: number) => api.get(`/pets?owner_id=${ownerId}`).then(res => res.data),
  getById: (id: number) => api.get(`/pets/${id}`).then(res => res.data),
  create: (data: any) => api.post('/pets', data).then(res => res.data),
  update: (id: number, data: any) => api.patch(`/pets/${id}`, data).then(res => res.data),
  delete: (id: number) => api.delete(`/pets/${id}`).then(res => res.data),
}

// 路由配置
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/Home.vue')
    },
    {
      path: '/welcome',
      name: 'welcome',
      component: () => import('../views/Welcome.vue')
    },
    {
      path: '/task-applications',
      name: 'task-applications',
      component: () => import('../views/TaskApplications.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/Register.vue')
    },
    {
      path: '/owner/signin',
      name: 'owner-signin',
      component: () => import('../views/OwnerSignIn.vue')
    },
    {
      path: '/nanny/signin',
      name: 'nanny-signin',
      component: () => import('../views/NannySignIn.vue')
    },
    {
      path: '/create-task',
      name: 'create-task',
      component: () => import('../views/CreateTask.vue')
    },
    {
      path: '/browse-task',
      name: 'browse-task',
      component: () => import('../views/BrowseTask.vue')
    },
    {
      path: '/apply-task/:id',
      name: 'apply-task',
      component: () => import('../views/ApplyForTask.vue')
    },
    {
      path: '/notification',
      name: 'notification',
      component: () => import('../views/Notification.vue')
    },
    {
      path: '/notification-from-owner',
      name: 'notification-from-owner',
      component: () => import('../views/NotificationFromOwner.vue')
    },
    {
      path: '/square',
      name: 'square',
      component: () => import('../views/Square.vue')
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/Profile.vue')
    },
    {
      path: '/my-applications',
      name: 'my-applications',
      component: () => import('../views/MyApplications.vue')
    },
    {
      path: '/edit-application/:id',
      name: 'edit-application',
      component: () => import('../views/EditApplication.vue')
    },
    {
      path: '/manage',
      name: 'manage',
      component: () => import('../views/Manage.vue')
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/Admin.vue')
    },
    {
      path: '/admin/signin',
      name: 'admin-signin',
      component: () => import('../views/AdminSignIn.vue')
    },
    {
      path: '/admin/users',
      name: 'admin-users',
      component: () => import('../views/AdminUsers.vue')
    },
    {
      path: '/admin/tasks',
      name: 'admin-tasks',
      component: () => import('../views/AdminTaskList.vue')
    },
    {
      path: '/admin/applications',
      name: 'admin-applications',
      component: () => import('../views/AdminApplicationList.vue')
    },
    {
      path: '/admin/owners',
      name: 'admin-owners',
      component: () => import('../views/AdminOwnerList.vue')
    },
    {
      path: '/admin/flyers',
      name: 'admin-flyers',
      component: () => import('../views/AdminFlyerList.vue')
    }
  ]
})

export default router
