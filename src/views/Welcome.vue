<template>
  <div class="min-h-screen pb-20">
    <!-- 欢迎头部 -->
    <div class="bg-gradient-to-br from-orange-400 to-amber-500 text-white p-6">
      <h2 class="text-2xl font-bold mb-1">欢迎回来！👋</h2>
      <p class="text-white/80">查看您的宠物动态</p>
    </div>

    <!-- 宠物列表 -->
    <div class="p-4">
      <div v-if="pets.length > 0" class="space-y-4">
        <div 
          v-for="pet in pets" 
          :key="pet.id"
          class="bg-white rounded-2xl overflow-hidden shadow-sm"
        >
          <!-- 宠物图片 -->
          <div class="h-48 bg-gradient-to-br from-orange-100 to-amber-100 flex items-center justify-center">
            <span class="text-8xl">
              {{ pet.pet_type === 'DOG' ? '🐕' : '🐱' }}
            </span>
          </div>
          
          <!-- 宠物信息 -->
          <div class="p-4">
            <div class="flex justify-between items-start mb-3">
              <div>
                <h3 class="text-xl font-bold text-gray-800">{{ pet.name }}</h3>
                <p class="text-sm text-gray-500">{{ pet.breed }}</p>
              </div>
              <span class="px-3 py-1 bg-orange-100 text-orange-500 text-xs font-bold rounded-full">
                {{ pet.pet_type === 'DOG' ? '狗狗' : '猫咪' }}
              </span>
            </div>
            
            <!-- 基本信息 -->
            <div class="flex gap-4 text-sm text-gray-500 mb-3">
              <span>⚖️ {{ pet.weight }}kg</span>
              <span>🎂 {{ pet.age_months }}个月</span>
              <span>🐾 {{ pet.gender === 'Male' ? '弟弟' : '妹妹' }}</span>
            </div>
            
            <!-- 健康信息 -->
            <div class="flex gap-2">
              <span v-if="pet.vaccination_record" class="px-2 py-1 bg-green-100 text-green-600 text-xs rounded-full">
                ✅ 疫苗已完成
              </span>
              <span v-if="pet.health_cert" class="px-2 py-1 bg-blue-100 text-blue-600 text-xs rounded-full">
                🏥 健康
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 无宠物 -->
      <div v-else class="text-center py-12">
        <span class="text-6xl block mb-4">🐾</span>
        <p class="text-gray-400 mb-4">暂无宠物信息</p>
        <button class="bg-gradient-to-br from-orange-400 to-amber-500 text-white px-6 py-3 rounded-full font-bold">
          + 添加宠物
        </button>
      </div>
    </div>

    <!-- 最近动态 -->
    <div class="p-4" v-if="tasks.length > 0">
      <h3 class="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3">最近任务</h3>
      <div class="space-y-3">
        <div 
          v-for="task in tasks.slice(0, 3)" 
          :key="task.id"
          class="bg-white rounded-xl p-4 shadow-sm"
        >
          <div class="flex justify-between items-center">
            <div>
              <p class="font-bold text-gray-800">{{ task.from_city }} → {{ task.to_city }}</p>
              <p class="text-sm text-gray-400">{{ task.travel_date }}</p>
            </div>
            <span 
              :class="{
                'bg-green-100 text-green-600': task.status === 'OPEN',
                'bg-yellow-100 text-yellow-600': task.status === 'SELECTING',
                'bg-blue-100 text-blue-600': task.status === 'CONFIRMED'
              }"
              class="px-3 py-1 text-xs font-bold rounded-full"
            >
              {{ task.status === 'OPEN' ? '招募中' : task.status === 'SELECTING' ? '选择中' : '已确认' }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { petApi, taskApi } from '../router'

interface Pet {
  id: number
  name: string
  pet_type: string
  breed: string
  weight: number
  age_months: number
  gender: string
  vaccination_record: string
  health_cert: string
}

interface Task {
  id: number
  from_city: string
  to_city: string
  travel_date: string
  status: string
}

const pets = ref<Pet[]>([])
const tasks = ref<Task[]>([])

const loadData = async () => {
  const savedUser = localStorage.getItem('petfly_user')
  if (savedUser) {
    const user = JSON.parse(savedUser)
    
    // 加载宠物
    try {
      const petData = await petApi.getMy(user.id)
      pets.value = petData
    } catch (e) {
      console.error('获取宠物失败:', e)
    }
    
    // 加载任务
    try {
      const taskData = await taskApi.getMy(user.id)
      tasks.value = taskData
    } catch (e) {
      console.error('获取任务失败:', e)
    }
  }
}

onMounted(() => {
  loadData()
})
</script>
