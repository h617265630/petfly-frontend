<template>
  <div class="min-h-screen pb-20">
    <!-- 头部 -->
    <div class="bg-gradient-to-br from-orange-400 to-amber-500 text-white p-6">
      <h2 class="text-xl font-bold">📋 申请列表</h2>
      <p class="text-white/80 text-sm">查看谁申请了您的任务</p>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="p-4 text-center py-12">
      <span class="text-gray-400">加载中...</span>
    </div>

    <!-- 任务列表 -->
    <div v-else class="p-4 space-y-6">
      <div 
        v-for="task in tasksWithApplications" 
        :key="task.id"
        class="bg-white rounded-2xl overflow-hidden shadow-sm"
      >
        <!-- 任务信息 -->
        <div class="p-4 border-b border-gray-100">
          <div class="flex justify-between items-start">
            <div>
              <h3 class="font-bold text-gray-800">{{ task.from_city }} → {{ task.to_city }}</h3>
              <p class="text-sm text-gray-400">📅 {{ task.travel_date }}</p>
            </div>
            <span 
              :class="{
                'bg-green-100 text-green-600': task.status === 'OPEN',
                'bg-yellow-100 text-yellow-600': task.status === 'SELECTING',
                'bg-blue-100 text-blue-600': task.status === 'CONFIRMED'
              }"
              class="px-3 py-1 text-xs font-bold rounded-full"
            >
              {{ task.status === 'OPEN' ? '招募中' : 
                 task.status === 'SELECTING' ? '选择中' : '已确认' }}
            </span>
          </div>
        </div>

        <!-- 申请列表 -->
        <div class="p-4 space-y-3">
          <h4 class="text-sm font-bold text-gray-500">申请人：</h4>
          
          <div 
            v-for="app in task.applications" 
            :key="app.id"
            class="bg-gray-50 rounded-xl p-3"
          >
            <div class="flex justify-between items-start mb-2">
              <div>
                <p class="font-bold text-gray-800">{{ app.flyer_name }}</p>
                <p class="text-xs text-gray-400">{{ app.flyer_from }} → {{ app.flyer_to }}</p>
              </div>
              <span 
                :class="{
                  'bg-yellow-100 text-yellow-600': app.status === 'PENDING',
                  'bg-blue-100 text-blue-600': app.status === 'SHORTLISTED',
                  'bg-green-100 text-green-600': app.status === 'ACCEPTED',
                  'bg-gray-100 text-gray-500': app.status === 'REJECTED'
                }"
                class="px-2 py-1 text-xs font-bold rounded-full"
              >
                {{ app.status === 'PENDING' ? '待审核' : 
                   app.status === 'SHORTLISTED' ? '已入围' : 
                   app.status === 'ACCEPTED' ? '已接受' : '已拒绝' }}
              </span>
            </div>
            
            <p class="text-sm text-gray-600 mb-2">{{ app.introduction }}</p>
            
            <div class="flex justify-between items-center">
              <span class="text-sm font-bold text-green-500">💰 {{ app.expected_price }}元</span>
              
              <div class="flex gap-2" v-if="app.status === 'PENDING'">
                <button 
                  @click="handleAccept(app, task)"
                  class="px-3 py-1 bg-green-500 text-white text-xs font-bold rounded-full"
                >
                  接受
                </button>
                <button 
                  @click="handleReject(app)"
                  class="px-3 py-1 bg-gray-300 text-gray-600 text-xs font-bold rounded-full"
                >
                  拒绝
                </button>
              </div>
            </div>
          </div>

          <div v-if="task.applications.length === 0" class="text-center py-4 text-gray-400 text-sm">
            暂无申请
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="!loading && tasksWithApplications.length === 0" class="text-center py-12">
      <span class="text-6xl block mb-4">📋</span>
      <p class="text-gray-400">您还没有发布任务</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { taskApi, applicationApi, userApi } from '../router'

interface TaskApplication {
  id: number
  task_id: number
  flyer_id: number
  flyer_name: string
  flyer_from: string
  flyer_to: string
  travel_date: string
  introduction: string
  expected_price: number
  status: string
}

interface TaskWithApps {
  id: number
  from_city: string
  to_city: string
  travel_date: string
  status: string
  applications: TaskApplication[]
}

const loading = ref(true)
const tasksWithApplications = ref<TaskWithApps[]>([])

const loadData = async () => {
  const savedUser = localStorage.getItem('petfly_user')
  if (!savedUser) {
    loading.value = false
    return
  }
  const user = JSON.parse(savedUser)

  try {
    // 获取我发布的任务
    const tasks = await taskApi.getMy(user.id)
    
    // 获取每个任务的申请
    const tasksWithApps = []
    for (const task of tasks) {
      const applications = await applicationApi.getByTask(task.id)
      
      // 获取每个申请者的信息
      const appsWithFlyerInfo = []
      for (const app of applications) {
        const flyer = await userApi.getById(app.flyer_id)
        appsWithFlyerInfo.push({
          ...app,
          flyer_name: flyer?.name || '未知',
          flyer_from: app.from_city,
          flyer_to: app.to_city
        })
      }
      
      tasksWithApps.push({
        ...task,
        applications: appsWithFlyerInfo
      })
    }
    
    tasksWithApplications.value = tasksWithApps
  } catch (e) {
    console.error('获取数据失败:', e)
  }
  loading.value = false
}

const handleAccept = async (app: TaskApplication, task: TaskWithApps) => {
  if (!confirm('确定接受该申请吗？')) return
  
  try {
    // 更新申请状态
    await applicationApi.updateStatus(app.id, 'SHORTLISTED')
    
    // 更新任务状态
    await taskApi.update(task.id, {
      status: 'SELECTING',
      selected_flyer_id: app.flyer_id
    })
    
    alert('已接受申请！')
    loadData()
  } catch (e) {
    console.error('操作失败:', e)
    alert('操作失败，请稍后重试')
  }
}

const handleReject = async (app: TaskApplication) => {
  if (!confirm('确定拒绝该申请吗？')) return
  
  try {
    await applicationApi.updateStatus(app.id, 'REJECTED')
    alert('已拒绝申请')
    loadData()
  } catch (e) {
    console.error('操作失败:', e)
    alert('操作失败，请稍后重试')
  }
}

onMounted(() => {
  loadData()
})
</script>
