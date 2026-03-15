<template>
  <div class="min-h-screen pb-20">
    <!-- 头部 -->
    <div class="bg-gradient-to-br from-green-400 to-emerald-500 text-white p-6">
      <h2 class="text-xl font-bold">我的申请 📋</h2>
      <p class="text-white/80 text-sm">查看您的申请记录</p>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="p-4 text-center py-12">
      <span class="text-gray-400">加载中...</span>
    </div>

    <!-- 申请列表 -->
    <div v-else class="p-4 space-y-4">
      <div 
        v-for="app in applications" 
        :key="app.id"
        @click="goToEdit(app.id)"
        class="bg-white rounded-2xl p-4 shadow-sm cursor-pointer"
      >
        <div class="flex justify-between items-start mb-3">
          <div>
            <h3 class="font-bold text-gray-800">
              {{ app.from_city }} → {{ app.to_city }}
            </h3>
            <p class="text-sm text-gray-400">📅 {{ app.travel_date }}</p>
          </div>
          <span 
            :class="{
              'bg-yellow-100 text-yellow-600': app.status === 'PENDING',
              'bg-blue-100 text-blue-600': app.status === 'SHORTLISTED',
              'bg-green-100 text-green-600': app.status === 'ACCEPTED',
              'bg-gray-100 text-gray-500': app.status === 'REJECTED'
            }"
            class="px-3 py-1 text-xs font-bold rounded-full"
          >
            {{ app.status === 'PENDING' ? '待审核' : 
               app.status === 'SHORTLISTED' ? '已入围' : 
               app.status === 'ACCEPTED' ? '已接受' : '已拒绝' }}
          </span>
        </div>
        
        <!-- 航班信息 -->
        <div class="text-sm text-gray-500 mb-2">
          <span v-if="app.flight_number">✈️ {{ app.flight_number }}</span>
        </div>
        
        <!-- 自我介绍 -->
        <p class="text-sm text-gray-600 mb-3">{{ app.introduction }}</p>
        
        <!-- 期望报酬 -->
        <div class="flex justify-between items-center">
          <span class="text-sm font-bold text-green-500">💰 {{ app.expected_price }}元</span>
          <span class="text-xs text-gray-400">{{ formatTime(app.created_at) }}</span>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="!loading && applications.length === 0" class="text-center py-12">
      <span class="text-6xl block mb-4">📋</span>
      <p class="text-gray-400 mb-4">暂无申请记录</p>
      <button 
        @click="goToBrowse"
        class="bg-gradient-to-br from-green-400 to-emerald-500 text-white px-6 py-3 rounded-full font-bold"
      >
        浏览任务
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { applicationApi } from '../router'

interface Application {
  id: number
  task_id: number
  from_city: string
  to_city: string
  travel_date: string
  flight_number: string
  introduction: string
  expected_price: number
  status: string
  created_at: string
}

const loading = ref(true)
const applications = ref<Application[]>([])

const formatTime = (time: string) => {
  if (!time) return ''
  const date = new Date(time)
  return date.toLocaleDateString('zh-CN')
}

const goToBrowse = () => {
  window.location.href = '/browse-task'
}

const goToEdit = (id: number) => {
  window.location.href = '/edit-application/' + id
}

onMounted(async () => {
  const savedUser = localStorage.getItem('petfly_user')
  if (savedUser) {
    const user = JSON.parse(savedUser)
    try {
      const data = await applicationApi.getMy(user.id)
      applications.value = data
    } catch (e) {
      console.error('获取申请失败:', e)
    }
  }
  loading.value = false
})
</script>
