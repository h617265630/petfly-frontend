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
      <h1 class="text-xl font-bold text-gray-700 mb-6">✏️ 修改申请</h1>

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
            placeholder="请介绍一下自己，例如：有多年养宠经验..."
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
        <div class="flex gap-3">
          <button 
            type="button"
            @click="handleDelete"
            class="flex-1 py-4 rounded-2xl font-bold text-white bg-red-400 shadow-lg hover:scale-[1.02] active:scale-[0.98] transition-all"
          >
            删除申请
          </button>
          <button 
            type="submit"
            class="flex-1 py-4 rounded-2xl font-bold text-white bg-gradient-to-br from-green-400 to-emerald-500 shadow-lg hover:scale-[1.02] active:scale-[0.98] transition-all"
          >
            保存修改
          </button>
        </div>

      </form>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { applicationApi } from '../router'

const route = useRoute()
const router = useRouter()
const applicationId = route.params.id

const from = ref('')
const to = ref('')
const date = ref('')
const flightNumber = ref('')
const introduction = ref('')
const expectedPrice = ref<number>(0)

const loadApplication = async () => {
  try {
    // 通过任务ID获取申请
    const data = await applicationApi.getApplicationById(Number(applicationId))
    if (data) {
      from.value = data.from_city || ''
      to.value = data.to_city || ''
      date.value = data.travel_date || ''
      flightNumber.value = data.flight_number || ''
      introduction.value = data.introduction || ''
      expectedPrice.value = data.expected_price || 0
    }
  } catch (e) {
    console.error('获取申请失败:', e)
  }
}

const handleSubmit = async () => {
  if (!from.value || !to.value || !date.value || !introduction.value) {
    alert('请填写完整信息')
    return
  }

  try {
    await applicationApi.update(Number(applicationId), {
      from_city: from.value,
      to_city: to.value,
      travel_date: date.value,
      flight_number: flightNumber.value,
      introduction: introduction.value,
      expected_price: expectedPrice.value
    })
    alert('修改成功！')
    router.back()
  } catch (e) {
    console.error('修改失败:', e)
    alert('修改失败，请稍后重试')
  }
}

const handleDelete = async () => {
  if (!confirm('确定要删除这条申请吗？')) return
  
  try {
    await applicationApi.delete(Number(applicationId))
    alert('删除成功！')
    router.push('/my-applications')
  } catch (e) {
    console.error('删除失败:', e)
    alert('删除失败，请稍后重试')
  }
}

onMounted(() => {
  loadApplication()
})
</script>
