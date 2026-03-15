<template>
  <div class="min-h-screen pb-16 bg-gradient-to-b from-amber-50 via-orange-50 to-pink-50 py-6 px-4">
    
    <!-- 返回 -->
    <div class="max-w-lg mx-auto mb-4">
      <button 
        @click="$router.back()" 
        class="text-gray-400 hover:text-gray-600 transition-colors flex items-center gap-2"
      >
        ← 返回
      </button>
    </div>

    <div class="max-w-lg mx-auto">
      <!-- 标题 -->
      <h1 class="text-xl font-bold text-center text-gray-700 mb-6">
        🔔 消息通知
      </h1>

      <!-- 加载状态 -->
      <div v-if="loading" class="text-center py-12">
        <span class="text-gray-400">加载中...</span>
      </div>

      <!-- 通知列表 -->
      <template v-if="!loading">
        <div class="space-y-3">
          <div 
            v-for="item in notifications" 
            :key="item.id"
            @click="handleClick(item)"
            :class="[
              'bg-white rounded-2xl p-4 shadow-[4px_4px_10px_rgba(0,0,0,0.05)] cursor-pointer hover:shadow-md transition-all',
              !item.is_read ? 'border-l-4 border-orange-400' : ''
            ]"
          >
            <div class="flex items-start gap-3">
              <!-- 图标 -->
              <div 
                :class="[
                  'w-10 h-10 rounded-full flex items-center justify-center text-lg',
                  item.type === 'SELECTED' ? 'bg-green-100' : 
                  item.type === 'APPLICATION_NEW' ? 'bg-blue-100' : 'bg-orange-100'
                ]"
              >
                {{ item.type === 'SELECTED' ? '✅' : item.type === 'APPLICATION_NEW' ? '💬' : '🔔' }}
              </div>
              
              <!-- 内容 -->
              <div class="flex-1">
                <div class="flex justify-between items-start">
                  <h3 :class="['font-bold text-sm', !item.is_read ? 'text-gray-800' : 'text-gray-500']">
                    {{ item.title }}
                  </h3>
                  <span class="text-xs text-gray-400">{{ formatTime(item.created_at) }}</span>
                </div>
                <p class="text-xs text-gray-400 mt-1 line-clamp-2">{{ item.content }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-if="notifications.length === 0" class="text-center py-12">
          <span class="text-4xl block mb-4">🔕</span>
          <p class="text-gray-400 text-sm">暂无新消息</p>
        </div>
      </template>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { notificationApi } from '../router'

interface Notification {
  id: number
  type: string
  title: string
  content: string
  is_read: number
  created_at: string
}

const loading = ref(true)
const notifications = ref<Notification[]>([])

// 当前用户 ID（演示用）
const currentUserId = 1

const formatTime = (time: string) => {
  const date = new Date(time)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const hours = Math.floor(diff / (1000 * 60 * 60))
  if (hours < 1) return '刚刚'
  if (hours < 24) return `${hours}小时前`
  const days = Math.floor(hours / 24)
  if (days < 7) return `${days}天前`
  return time.split('T')[0]
}

const handleClick = async (item: Notification) => {
  if (!item.is_read) {
    await notificationApi.markAsRead(item.id)
    item.is_read = 1
  }
}

onMounted(async () => {
  try {
    const data = await notificationApi.getByUser(currentUserId)
    notifications.value = data
  } catch (e) {
    console.error('获取通知失败:', e)
  } finally {
    loading.value = false
  }
})
</script>
