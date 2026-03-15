<template>
  <div class="min-h-screen pb-20">
    <!-- 头部 -->
    <div class="bg-gradient-to-br from-purple-400 to-indigo-500 text-white p-6">
      <h2 class="text-xl font-bold">⚙️ 管理后台</h2>
      <p class="text-white/80 text-sm">审核管理</p>
    </div>

    <!-- 待审核任务 -->
    <div class="p-4">
      <h3 class="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3">待审核任务</h3>      
      <div v-if="pendingTasks.length > 0" class="space-y-4">
        <div 
          v-for="task in pendingTasks" 
          :key="task.id"
          class="bg-white rounded-2xl overflow-hidden shadow-sm"
        >
          <!-- 任务基本信息 -->
          <div class="p-4 border-b border-gray-100">
            <div class="flex justify-between items-start mb-3">
              <div>
                <p class="font-bold text-lg text-gray-800">{{ task.from_city }} → {{ task.to_city }}</p>
                <p class="text-sm text-gray-400">📅 {{ task.travel_date }}</p>
              </div>
              <span class="px-3 py-1 bg-yellow-100 text-yellow-600 text-xs font-bold rounded-full">
                待确认
              </span>
            </div>
          </div>

          <!-- 主人信息 -->
          <div class="p-4 border-b border-gray-100 bg-orange-50">
            <h4 class="text-xs font-bold text-orange-600 uppercase mb-2">🐕 主人信息</h4>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span class="text-gray-400">姓名：</span>
                <span class="font-bold">{{ task.owner?.name || '未知' }}</span>
              </div>
              <div>
                <span class="text-gray-400">电话：</span>
                <span class="font-bold">{{ task.owner?.phone || '未知' }}</span>
              </div>
              <div>
                <span class="text-gray-400">微信：</span>
                <span class="font-bold">{{ task.owner?.wechat || '未填写' }}</span>
              </div>
            </div>
          </div>

          <!-- 宠物信息 -->
          <div v-if="task.pet" class="p-4 border-b border-gray-100">
            <h4 class="text-xs font-bold text-purple-600 uppercase mb-2">🐾 宠物信息</h4>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span class="text-gray-400">名字：</span>
                <span class="font-bold">{{ task.pet.name || '未知' }}</span>
              </div>
              <div>
                <span class="text-gray-400">类型：</span>
                <span class="font-bold">{{ task.pet.pet_type === 'DOG' ? '🐕 狗狗' : '🐱 猫咪' }}</span>
              </div>
              <div>
                <span class="text-gray-400">品种：</span>
                <span class="font-bold">{{ task.pet.breed || '未知' }}</span>
              </div>
              <div>
                <span class="text-gray-400">体重：</span>
                <span class="font-bold">{{ task.pet.weight || '未知' }}kg</span>
              </div>
            </div>
          </div>

          <!-- 陪飞员信息 -->
          <div v-if="task.selectedFlyer" class="p-4 border-b border-gray-100 bg-green-50">
            <h4 class="text-xs font-bold text-green-600 uppercase mb-2">✈️ 陪飞员信息</h4>
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span class="text-gray-400">姓名：</span>
                <span class="font-bold">{{ task.selectedFlyer.name || '未知' }}</span>
              </div>
              <div>
                <span class="text-gray-400">电话：</span>
                <span class="font-bold">{{ task.selectedFlyer.phone || '未知' }}</span>
              </div>
              <div>
                <span class="text-gray-400">微信：</span>
                <span class="font-bold">{{ task.selectedFlyer.wechat || '未填写' }}</span>
              </div>
              <div>
                <span class="text-gray-400">期望报酬：</span>
                <span class="font-bold text-green-600">{{ task.selectedApp?.expected_price || '未知' }}元</span>
              </div>
            </div>
            
            <!-- 陪飞员申请详情 -->
            <div v-if="task.selectedApp" class="mt-3 pt-3 border-t border-green-200">
              <div class="text-sm">
                <div class="mb-1">
                  <span class="text-gray-400">航线：</span>
                  <span class="font-bold">{{ task.selectedApp.from_city }} → {{ task.selectedApp.to_city }}</span>
                </div>
                <div v-if="task.selectedApp.flight_number" class="mb-1">
                  <span class="text-gray-400">航班：</span>
                  <span class="font-bold">{{ task.selectedApp.flight_number }}</span>
                </div>
                <div class="mb-1">
                  <span class="text-gray-400">自我介绍：</span>
                  <span class="text-gray-600">{{ task.selectedApp.introduction }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 预算 -->
          <div class="p-4 bg-gray-50">
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-500">任务预算</span>
              <span class="text-xl font-bold text-green-600">{{ task.budget_min }}-{{ task.budget_max }}元</span>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="p-4 flex gap-3">
            <button 
              @click="confirmTask(task)"
              class="flex-1 py-3 bg-green-500 text-white font-bold rounded-xl"
            >
              ✅ 确认通过
            </button>
            <button 
              @click="rejectTask(task)"
              class="flex-1 py-3 bg-gray-300 text-gray-600 font-bold rounded-xl"
            >
              ❌ 拒绝
            </button>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-12 bg-white rounded-2xl">
        <span class="text-5xl block mb-3">✅</span>
        <p class="text-gray-400">暂无待审核任务</p>
      </div>
    </div>

    <!-- 统计 -->
    <div class="p-4">
      <h3 class="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3">数据统计</h3>
      
      <div class="grid grid-cols-2 gap-3">
        <div 
          @click="goTo('/admin/tasks')"
          class="bg-white rounded-2xl p-4 shadow-sm text-center cursor-pointer hover:bg-gray-50"
        >
          <p class="text-2xl font-bold text-blue-500">{{ stats.taskCount }}</p>
          <p class="text-xs text-gray-400">任务总数</p>
        </div>
        <div 
          @click="goTo('/admin/applications')"
          class="bg-white rounded-2xl p-4 shadow-sm text-center cursor-pointer hover:bg-gray-50"
        >
          <p class="text-2xl font-bold text-purple-500">{{ stats.appCount }}</p>
          <p class="text-xs text-gray-400">申请总数</p>
        </div>
        <div 
          @click="goTo('/admin/owners')"
          class="bg-white rounded-2xl p-4 shadow-sm text-center cursor-pointer hover:bg-gray-50"
        >
          <p class="text-2xl font-bold text-orange-500">{{ stats.ownerCount }}</p>
          <p class="text-xs text-gray-400">主人数量</p>
        </div>
        <div 
          @click="goTo('/admin/flyers')"
          class="bg-white rounded-2xl p-4 shadow-sm text-center cursor-pointer hover:bg-gray-50"
        >
          <p class="text-2xl font-bold text-green-500">{{ stats.flyerCount }}</p>
          <p class="text-xs text-gray-400">陪飞员数量</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { userApi, taskApi, applicationApi } from '../router'

const pendingTasks = ref<any[]>([])
const stats = ref({
  ownerCount: 0,
  flyerCount: 0,
  taskCount: 0,
  appCount: 0
})

const goTo = (path: string) => {
  window.location.href = path
}

const loadData = async () => {
  try {
    const allUsers = await userApi.getAll()
    const usersMap: any = {}
    allUsers.forEach((u: any) => { usersMap[u.id] = u })
    
    stats.value.ownerCount = allUsers.filter((u: any) => u.role === 'OWNER').length
    stats.value.flyerCount = allUsers.filter((u: any) => u.role === 'FLYER').length
    
    const allTasks = await taskApi.getAll()
    stats.value.taskCount = allTasks.length
    
    const pending = allTasks.filter((t: any) => t.status === 'SELECTING')
    
    const detailedTasks = []
    for (const task of pending) {
      const owner = usersMap[task.owner_id] || null
      
      let pet = null
      if (task.pet_id) {
        try {
          pet = await (await fetch(`http://192.168.18.35:3001/pets/${task.pet_id}`)).json()
        } catch (e) {}
      }
      
      let selectedFlyer = null
      let selectedApp = null
      if (task.selected_flyer_id) {
        selectedFlyer = usersMap[task.selected_flyer_id] || null
        const apps = await applicationApi.getByTask(task.id)
        selectedApp = apps.find((a: any) => a.flyer_id === task.selected_flyer_id)
      }
      
      detailedTasks.push({ ...task, owner, pet, selectedFlyer, selectedApp })
    }
    
    pendingTasks.value = detailedTasks
    
    const allApps = await applicationApi.getAll()
    stats.value.appCount = allApps.length
  } catch (e) {
    console.error('获取数据失败:', e)
  }
}

const confirmTask = async (task: any) => {
  if (!confirm('确认通过该任务？')) return
  try {
    await taskApi.update(task.id, { status: 'CONFIRMED' })
    alert('确认成功！')
    loadData()
  } catch (e) {
    alert('操作失败')
  }
}

const rejectTask = async (task: any) => {
  if (!confirm('拒绝该任务？')) return
  try {
    await taskApi.update(task.id, { status: 'CANCELLED' })
    alert('已拒绝！')
    loadData()
  } catch (e) {
    alert('操作失败')
  }
}

onMounted(() => {
  loadData()
})
</script>
