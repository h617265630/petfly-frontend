<template>
  <div class="min-h-screen bg-gray-50 pb-20">
    <!-- 头部 -->
    <div 
      class="p-6 text-center"
      :class="user?.role === 'OWNER' ? 'bg-gradient-to-br from-orange-400 to-amber-500' : 'bg-gradient-to-br from-green-400 to-emerald-500'"
    >
      <div class="w-20 h-20 bg-white/20 rounded-full mx-auto mb-3 flex items-center justify-center text-4xl">
        {{ user?.role === 'OWNER' ? '👤' : '✈️' }}
      </div>
      <h2 class="text-xl font-bold">{{ user?.name || '用户' }}</h2>
      <p class="text-white/80 text-sm">{{ user?.role === 'OWNER' ? '宠物主人' : '陪飞员' }}</p>
    </div>

    <!-- 宠物信息 (Owner) -->
    <div v-if="user?.role === 'OWNER'" class="p-4">
      <h3 class="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3">我的宠物</h3>
      
      <div v-if="pets.length > 0" class="space-y-3">
        <div 
          v-for="pet in pets" 
          :key="pet.id"
          class="bg-white rounded-2xl p-4 shadow-sm"
        >
          <div class="flex items-center gap-4">
            <div class="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center text-3xl">
              {{ pet.pet_type === 'DOG' ? '🐕' : '🐱' }}
            </div>
            <div class="flex-1">
              <h4 class="font-bold text-gray-800">{{ pet.name }}</h4>
              <p class="text-sm text-gray-500">{{ pet.breed }}</p>
              <div class="flex gap-3 mt-1">
                <span class="text-xs text-gray-400">体重: {{ pet.weight }}kg</span>
                <span class="text-xs text-gray-400">年龄: {{ pet.age_months }}个月</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="bg-white rounded-2xl p-6 text-center shadow-sm">
        <span class="text-4xl block mb-2">🐾</span>
        <p class="text-gray-400 text-sm">暂无宠物信息</p>
        <button class="mt-3 text-orange-500 text-sm font-bold">+ 添加宠物</button>
      </div>
    </div>

    <!-- 陪飞员信息 (Flyer) -->
    <div v-else-if="user?.role === 'FLYER'" class="p-4">
      <h3 class="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3">我的资料</h3>
      
      <div class="bg-white rounded-2xl p-4 shadow-sm space-y-3">
        <div class="flex justify-between items-center py-2 border-b border-gray-100">
          <span class="text-gray-500">认证状态</span>
          <span :class="flyerProfile?.is_verified ? 'text-green-500' : 'text-gray-400'" class="font-bold">
            {{ flyerProfile?.is_verified ? '✅ 已认证' : '⏳ 待认证' }}
          </span>
        </div>
        <div class="flex justify-between items-center py-2 border-b border-gray-100">
          <span class="text-gray-500">护照姓名</span>
          <span class="text-gray-800">{{ flyerProfile?.passport_name || '未填写' }}</span>
        </div>
        <div class="flex justify-between items-center py-2 border-b border-gray-100">
          <span class="text-gray-500">签证类型</span>
          <span class="text-gray-800">{{ flyerProfile?.visa_type || '未填写' }}</span>
        </div>
        <div class="flex justify-between items-center py-2 border-b border-gray-100">
          <span class="text-gray-500">养宠经验</span>
          <span class="text-gray-800">{{ flyerProfile?.has_pet_experience ? '有经验' : '无经验' }}</span>
        </div>
      </div>
    </div>

    <!-- 功能菜单 -->
    <div class="p-4">
      <h3 class="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3">设置</h3>
      
      <div class="bg-white rounded-2xl shadow-sm overflow-hidden">
        <div class="flex items-center justify-between p-4 border-b border-gray-100">
          <div class="flex items-center gap-3">
            <span class="text-gray-600">🔔</span>
            <span class="text-gray-800">消息通知</span>
          </div>
          <span class="text-gray-400">›</span>
        </div>
        <div class="flex items-center justify-between p-4 border-b border-gray-100">
          <div class="flex items-center gap-3">
            <span class="text-gray-600">🔒</span>
            <span class="text-gray-800">隐私设置</span>
          </div>
          <span class="text-gray-400">›</span>
        </div>
        <div class="flex items-center justify-between p-4 border-b border-gray-100">
          <div class="flex items-center gap-3">
            <span class="text-gray-600">❓</span>
            <span class="text-gray-800">帮助中心</span>
          </div>
          <span class="text-gray-400">›</span>
        </div>
        <div @click="handleLogout" class="flex items-center justify-between p-4">
          <div class="flex items-center gap-3">
            <span class="text-red-500">🚪</span>
            <span class="text-red-500">退出登录</span>
          </div>
          <span class="text-gray-400">›</span>
        </div>
      </div>
    </div>

    <!-- 版本信息 -->
    <div class="text-center text-gray-300 text-xs py-4">
      PET FLY v1.0.0
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { userApi, petApi } from '../router'

interface User {
  id: number
  name: string
  role: string
}

interface Pet {
  id: number
  name: string
  pet_type: string
  breed: string
  weight: number
  age_months: number
}

interface FlyerProfile {
  is_verified: number
  passport_name: string
  visa_type: string
  has_pet_experience: number
}

const user = ref<User | null>(null)
const pets = ref<Pet[]>([])
const flyerProfile = ref<FlyerProfile | null>(null)

const loadData = async () => {
  const savedUser = localStorage.getItem('petfly_user')
  if (savedUser) {
    user.value = JSON.parse(savedUser)
    
    // 加载宠物信息
    if (user.value?.role === 'OWNER') {
      try {
        const data = await petApi.getMy(user.value.id)
        pets.value = data
      } catch (e) {
        console.error('获取宠物失败:', e)
      }
    }
    
    // 加载陪飞员信息
    if (user.value?.role === 'FLYER') {
      try {
        const data = await userApi.getFlyerProfile(user.value.id)
        flyerProfile.value = data
      } catch (e) {
        console.error('获取陪飞员信息失败:', e)
      }
    }
  }
}

const handleLogout = () => {
  localStorage.removeItem('petfly_user')
  window.location.href = '/'
}

onMounted(() => {
  loadData()
})
</script>
