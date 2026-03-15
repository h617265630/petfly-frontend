<template>
  <div class="min-h-screen pb-16 bg-gradient-to-b from-green-50 via-emerald-50 to-teal-50 py-6 px-4">
    
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
        🔔 来自 PET OWNER 的消息
      </h1>

      <!-- 通知列表 -->
      <div class="space-y-3">
        <div 
          v-for="item in notifications" 
          :key="item.id"
          @click="handleClick(item)"
          :class="[
            'bg-white rounded-2xl p-4 shadow-[4px_4px_10px_rgba(0,0,0,0.05)] cursor-pointer hover:shadow-md transition-all',
            !item.read ? 'border-l-4 border-green-400' : ''
          ]"
        >
          <div class="flex items-start gap-3">
            <!-- 头像 -->
            <div class="w-12 h-12 rounded-full bg-gradient-to-br from-orange-100 to-amber-100 flex items-center justify-center text-xl">
              🐕
            </div>
            
            <!-- 内容 -->
            <div class="flex-1">
              <div class="flex justify-between items-start">
                <div>
                  <h3 :class="['font-bold text-sm', !item.read ? 'text-gray-800' : 'text-gray-500']">
                    {{ item.ownerName }}
                  </h3>
                  <p class="text-xs text-gray-400">{{ item.petName }} · {{ item.route }}</p>
                </div>
                <span class="text-xs text-gray-400">{{ item.time }}</span>
              </div>
              <p class="text-sm text-gray-600 mt-2 line-clamp-2">{{ item.content }}</p>
              
              <!-- 状态标签 -->
              <div class="flex gap-2 mt-3">
                <span 
                  v-if="item.status === 'pending'"
                  class="px-2 py-1 bg-yellow-100 text-yellow-600 text-xs font-bold rounded-full"
                >
                  待响应
                </span>
                <span 
                  v-if="item.status === 'accepted'"
                  class="px-2 py-1 bg-green-100 text-green-600 text-xs font-bold rounded-full"
                >
                  已接受
                </span>
                <span 
                  v-if="item.status === 'rejected'"
                  class="px-2 py-1 bg-gray-100 text-gray-500 text-xs font-bold rounded-full"
                >
                  已拒绝
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="notifications.length === 0" class="text-center py-12">
        <span class="text-4xl block mb-4">🔕</span>
        <p class="text-gray-400 text-sm">暂无新消息</p>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Notification {
  id: number
  ownerName: string
  petName: string
  route: string
  content: string
  time: string
  read: boolean
  status: 'pending' | 'accepted' | 'rejected'
}

const notifications = ref<Notification[]>([
  {
    id: 1,
    ownerName: '张三',
    petName: '豆豆',
    route: '上海 → 北京',
    content: '您好！看到您在接宠物单，请问3月20日上海到北京的可以接吗？',
    time: '10分钟前',
    read: false,
    status: 'pending'
  },
  {
    id: 2,
    ownerName: '李四',
    petName: '咪咪',
    route: '深圳 → 杭州',
    content: '我家猫咪很乖，有航空箱，请问可以办理随机托运吗？',
    time: '1小时前',
    read: false,
    status: 'pending'
  },
  {
    id: 3,
    ownerName: '王五',
    petName: '旺财',
    route: '广州 → 上海',
    content: '谢谢您接受我的请求！期待和您合作！',
    time: '昨天',
    read: true,
    status: 'accepted'
  },
  {
    id: 4,
    ownerName: '赵六',
    petName: '小橘',
    route: '成都 → 北京',
    content: '抱歉，我的行程有变，暂时不需要了',
    time: '昨天',
    read: true,
    status: 'rejected'
  }
])

const handleClick = (item: Notification) => {
  item.read = true
  console.log('点击通知:', item)
}
</script>
