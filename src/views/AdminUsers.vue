<template>
  <div class="min-h-screen pb-20">
    <!-- 头部 -->
    <div class="bg-gradient-to-br from-purple-400 to-indigo-500 text-white p-6">
      <h2 class="text-xl font-bold">👥 用户管理</h2>
      <p class="text-white/80 text-sm">查看所有用户</p>
    </div>

    <!-- 搜索 -->
    <div class="p-4">
      <input 
        v-model="searchKeyword"
        type="text"
        placeholder="搜索用户名或手机号..."
        class="w-full bg-white border-2 border-gray-200 rounded-xl py-3 px-4 text-gray-700 focus:outline-none focus:border-purple-400 transition-colors"
      />
    </div>

    <!-- 用户列表 -->
    <div class="p-4 space-y-3">
      <div 
        v-for="user in filteredUsers" 
        :key="user.id"
        class="bg-white rounded-2xl p-4 shadow-sm"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div 
              class="w-12 h-12 rounded-full flex items-center justify-center text-xl"
              :class="{
                'bg-orange-100': user.role === 'OWNER',
                'bg-green-100': user.role === 'FLYER',
                'bg-purple-100': user.role === 'MANAGER'
              }"
            >
              {{ user.role === 'OWNER' ? '🐕' : user.role === 'FLYER' ? '✈️' : '⚙️' }}
            </div>
            <div>
              <p class="font-bold text-gray-800">{{ user.name }}</p>
              <p class="text-xs text-gray-400">{{ user.phone }}</p>
            </div>
          </div>
          <span 
            :class="{
              'bg-orange-100 text-orange-600': user.role === 'OWNER',
              'bg-green-100 text-green-600': user.role === 'FLYER',
              'bg-purple-100 text-purple-600': user.role === 'MANAGER'
            }"
            class="px-3 py-1 text-xs font-bold rounded-full"
          >
            {{ user.role === 'OWNER' ? '主人' : user.role === 'FLYER' ? '陪飞员' : '管理员' }}
          </span>
        </div>

        <!-- 详细信息 -->
        <div class="mt-3 pt-3 border-t border-gray-100">
          <div class="grid grid-cols-2 gap-2 text-sm">
            <div>
              <span class="text-gray-400">微信：</span>
              <span class="font-bold">{{ user.wechat || '未填写' }}</span>
            </div>
            <div>
              <span class="text-gray-400">状态：</span>
              <span :class="user.status === 1 ? 'text-green-500' : 'text-red-500'" class="font-bold">
                {{ user.status === 1 ? '正常' : '禁用' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="filteredUsers.length === 0" class="text-center py-12">
      <span class="text-5xl block mb-3">🔍</span>
      <p class="text-gray-400">暂无用户</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { userApi } from '../router'

const users = ref<any[]>([])
const searchKeyword = ref('')

const filteredUsers = computed(() => {
  if (!searchKeyword.value) return users.value
  const keyword = searchKeyword.value.toLowerCase()
  return users.value.filter((u: any) => 
    u.name?.toLowerCase().includes(keyword) || 
    u.phone?.includes(keyword) ||
    u.wechat?.toLowerCase().includes(keyword)
  )
})

onMounted(async () => {
  try {
    users.value = await userApi.getAll()
  } catch (e) {
    console.error('获取用户失败:', e)
  }
})
</script>
