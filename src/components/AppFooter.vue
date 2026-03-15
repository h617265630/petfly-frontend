<template>
  <div class="fixed bottom-0 left-0 right-0 bg-white shadow-[0_-4px_12px_rgba(0,0,0,0.08)] safe-area-bottom">
    <!-- Owner 底部导航 -->
    <template v-if="role === 'OWNER'">
      <div class="flex justify-around items-center h-14">
        <!-- 欢迎 -->
        <div 
          @click="goTo('/welcome')"
          class="flex flex-col items-center justify-center flex-1 h-full"
          :class="active === '/welcome' ? 'text-orange-500' : 'text-gray-400'"
        >
          <span class="text-xl">🏠</span>
          <span class="text-xs font-bold">欢迎</span>
        </div>

        <!-- 发布任务 -->
        <div 
          @click="goTo('/create-task')"
          class="flex flex-col items-center justify-center flex-1 h-full"
          :class="active === '/create-task' ? 'text-orange-500' : 'text-gray-400'"
        >
          <span class="text-xl">➕</span>
          <span class="text-xs font-bold">发布</span>
        </div>

        <!-- 申请列表 -->
        <div 
          @click="goTo('/task-applications')"
          class="flex flex-col items-center justify-center flex-1 h-full"
          :class="active === '/task-applications' ? 'text-orange-500' : 'text-gray-400'"
        >
          <span class="text-xl">📋</span>
          <span class="text-xs font-bold">申请</span>
        </div>

        <!-- 消息
        <div 
          @click="goTo('/notification')"
          class="flex flex-col items-center justify-center flex-1 h-full relative"
          :class="active === '/notification' ? 'text-orange-500' : 'text-gray-400'"
        >
        >
          <span class="text-xl">🔔</span>
          <span class="text-xs font-bold">消息</span>
          <span v-if="unreadCount > 0" class="absolute top-1 right-1/3 w-2 h-2 bg-red-500 rounded-full"></span>
        </div>

        <!-- 我的 -->
        <div 
          @click="goTo('/profile')"
          class="flex flex-col items-center justify-center flex-1 h-full"
          :class="active === '/profile' ? 'text-orange-500' : 'text-gray-400'"
        >
          <span class="text-xl">👤</span>
          <span class="text-xs font-bold">我的</span>
        </div>
      </div>
    </template>

    <!-- Flyer Nanny 底部导航 -->
    <template v-else-if="role === 'FLYER'">
      <div class="flex justify-around items-center h-14">
        <!-- 浏览任务 -->
        <div 
          @click="goTo('/browse-task')"
          class="flex flex-col items-center justify-center flex-1 h-full"
          :class="active === '/browse-task' ? 'text-green-500' : 'text-gray-400'"
        >
          <span class="text-xl">🔍</span>
          <span class="text-xs font-bold">任务</span>
        </div>

        <!-- 我的申请 -->
        <div 
          @click="goTo('/my-applications')"
          class="flex flex-col items-center justify-center flex-1 h-full"
          :class="active === '/my-applications' ? 'text-green-500' : 'text-gray-400'"
        >
          <span class="text-xl">📋</span>
          <span class="text-xs font-bold">申请</span>
        </div>

        <!-- 消息 -->
        <div 
          @click="goTo('/notification-from-owner')"
          class="flex flex-col items-center justify-center flex-1 h-full relative"
          :class="active === '/notification-from-owner' ? 'text-green-500' : 'text-gray-400'"
        >
          <span class="text-xl">💬</span>
          <span class="text-xs font-bold">消息</span>
          <span v-if="unreadCount > 0" class="absolute top-1 right-1/3 w-2 h-2 bg-red-500 rounded-full"></span>
        </div>

        <!-- 我的 -->
        <div 
          @click="goTo('/profile')"
          class="flex flex-col items-center justify-center flex-1 h-full"
          :class="active === '/profile' ? 'text-green-500' : 'text-gray-400'"
        >
          <span class="text-xl">👤</span>
          <span class="text-xs font-bold">我的</span>
        </div>
      </div>
    </template>

    <!-- Admin 底部导航 -->
    <template v-else-if="role === 'MANAGER'">
      <div class="flex justify-around items-center h-14">
        <!-- 任务审核 -->
        <div 
          @click="goTo('/admin')"
          class="flex flex-col items-center justify-center flex-1 h-full"
          :class="active === '/admin' ? 'text-purple-500' : 'text-gray-400'"
        >
          <span class="text-xl">⚙️</span>
          <span class="text-xs font-bold">审核</span>
        </div>

        <!-- 用户管理 -->
        <div 
          @click="goTo('/admin/users')"
          class="flex flex-col items-center justify-center flex-1 h-full"
          :class="active === '/admin/users' ? 'text-purple-500' : 'text-gray-400'"
        >
          <span class="text-xl">👥</span>
          <span class="text-xs font-bold">用户</span>
        </div>

        <!-- 我的 -->
        <div 
          @click="goTo('/profile')"
          class="flex flex-col items-center justify-center flex-1 h-full"
          :class="active === '/profile' ? 'text-purple-500' : 'text-gray-400'"
        >
          <span class="text-xl">👤</span>
          <span class="text-xs font-bold">我的</span>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  role: 'OWNER' | 'FLYER' | 'MANAGER' | ''
  active: string
}>()

const unreadCount = ref(0)

const goTo = (path: string) => {
  window.location.href = path
}
</script>

<style scoped>
.safe-area-bottom {
  padding-bottom: env(safe-area-inset-bottom);
}
</style>
