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
      <!-- 任务详情 -->
      <div class="bg-white rounded-2xl p-5 shadow-sm mb-6">
        <h1 class="text-lg font-bold text-gray-700 mb-4">📋 任务详情</h1>
        
        <div class="space-y-3">
          <div class="flex justify-between">
            <span class="text-sm text-gray-400">宠物类型</span>
            <span class="text-sm font-bold text-gray-700">{{ task?.pet_type === 'DOG' ? '🐕 狗狗' : '🐱 猫咪' }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-sm text-gray-400">出发地</span>
            <span class="text-sm font-bold text-gray-700">{{ task?.from_city }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-sm text-gray-400">目的地</span>
            <span class="text-sm font-bold text-gray-700">{{ task?.to_city }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-sm text-gray-400">出行日期</span>
            <span class="text-sm font-bold text-gray-700">{{ task?.travel_date }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-sm text-gray-400">预算</span>
            <span class="text-sm font-bold text-green-500">{{ task?.budget_min }}-{{ task?.budget_max }}元</span>
          </div>
        </div>
      </div>

      <!-- 申请表单 -->
      <form @submit.prevent="handleSubmit" class="space-y-5">
        
        <!-- 您的行程 -->
        <div class="bg-white rounded-2xl p-5 shadow-sm">
          <h3 class="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">✈️ 您的行程</h3>
          
          <div class="mb-4">
            <label class="block text-xs font-bold text-gray-400 mb-2">出发地</label>
            <input 
              v-model="from"
              type="text"
              placeholder="例如：上海"
              class="w-full bg-white border-2 border-gray-200 rounded-xl py-3 px-4 text-gray-700 focus:outline-none focus:border-green-400 transition-colors"
            />
          </div>

          <div class="mb-4">
            <label class="block text-xs font-bold text-gray-400 mb-2">目的地</label>
            <input 
              v-model="to"
              type="text"
              placeholder="例如：北京"
              class="w-full bg-white border-2 border-gray-200 rounded-xl py-3 px-4 text-gray-700 focus:outline-none focus:border-green-400 transition-colors"
            />
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-400 mb-2">可出行日期</label>
            <input 
              v-model="date"
              type="date"
              class="w-full bg-white border-2 border-gray-200 rounded-xl py-3 px-4 text-gray-700 focus:outline-none focus:border-green-400 transition-colors"
            />
          </div>
        </div>

        <!-- 航班信息 -->
        <div class="bg-white rounded-2xl p-5 shadow-sm">
          <h3 class="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">🎫 航班信息（选填）</h3>
          
          <div>
            <label class="block text-xs font-bold text-gray-400 mb-2">航班号</label>
            <input 
              v-model="flightNumber"
              type="text"
              placeholder="例如：CA1234"
              class="w-full bg-white border-2 border-gray-200 rounded-xl py-3 px-4 text-gray-700 focus:outline-none focus:border-green-400 transition-colors"
            />
          </div>
        </div>

        <!-- 自我介绍 -->
        <div class="bg-white rounded-2xl p-5 shadow-sm">
          <h3 class="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">👋 自我介绍</h3>
          
          <textarea 
            v-model="introduction"
            placeholder="请介绍一下自己，例如：有多年养宠经验，曾帮助运送宠物..."
            rows="4"
            class="w-full bg-white border-2 border-gray-200 rounded-xl py-3 px-4 text-gray-700 focus:outline-none focus:border-green-400 transition-colors resize-none"
          ></textarea>
        </div>

        <!-- 期望报酬 -->
        <div class="bg-white rounded-2xl p-5 shadow-sm">
          <h3 class="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">💰 期望报酬</h3>
          
          <input 
            v-model="expectedPrice"
            type="number"
            placeholder="请输入期望报酬（元）"
            class="w-full bg-white border-2 border-gray-200 rounded-xl py-3 px-4 text-gray-700 focus:outline-none focus:border-green-400 transition-colors"
          />
        </div>

        <!-- 提交按钮 -->
        <button 
          type="submit"
          class="w-full py-4 rounded-2xl font-bold text-white tracking-wider bg-gradient-to-br from-green-400 to-emerald-500 shadow-lg hover:scale-[1.02] active:scale-[0.98] transition-all"
        >
          提交申请
        </button>

      </form>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { taskApi, applicationApi } from '../router'

const route = useRoute()
const taskId = route.params.id

const task = ref<any>(null)
const from = ref('')
const to = ref('')
const date = ref('')
const flightNumber = ref('')
const introduction = ref('')
const expectedPrice = ref<number>(0)

const loadTask = async () => {
  try {
    const data = await taskApi.getById(Number(taskId))
    task.value = data
    // 预填出发地和目的地
    if (data) {
      from.value = data.from_city || ''
      to.value = data.to_city || ''
      date.value = data.travel_date || ''
    }
  } catch (e) {
    console.error('获取任务失败:', e)
  }
}

const handleSubmit = async () => {
  if (!from.value || !to.value || !date.value || !introduction.value) {
    alert('请填写完整信息')
    return
  }

  const savedUser = localStorage.getItem('petfly_user')
  if (!savedUser) {
    alert('请先登录')
    return
  }
  const user = JSON.parse(savedUser)

  try {
    await applicationApi.create({
      task_id: Number(taskId),
      flyer_id: user.id,
      from_city: from.value,
      to_city: to.value,
      travel_date: date.value,
      flight_number: flightNumber.value,
      introduction: introduction.value,
      expected_price: expectedPrice.value,
      status: 'PENDING'
    })
    alert('申请提交成功！')
    window.location.href = '/my-applications'
  } catch (e) {
    console.error('提交申请失败:', e)
    alert('提交失败，请稍后重试')
  }
}

onMounted(() => {
  loadTask()
})
</script>
