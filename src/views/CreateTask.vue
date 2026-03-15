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
        🐕 发布宠物出行需求
      </h1>

      <form @submit.prevent="handleSubmit" class="space-y-5">
        
        <!-- 宠物信息 -->
        <div class="bg-white rounded-2xl p-5 shadow-sm">
          <h3 class="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">🐾 宠物信息</h3>
          
          <!-- 宠物类型 -->
          <div class="mb-4">
            <label class="block text-xs font-bold text-gray-400 mb-2">宠物类型</label>
            <div class="flex gap-3">
              <button 
                type="button"
                @click="petType = 'DOG'"
                :class="[
                  'flex-1 py-2 rounded-xl font-bold text-sm transition-all',
                  petType === 'DOG' ? 'bg-orange-500 text-white' : 'bg-gray-100 text-gray-600'
                ]"
              >
                🐕 狗狗
              </button>
              <button 
                type="button"
                @click="petType = 'CAT'"
                :class="[
                  'flex-1 py-2 rounded-xl font-bold text-sm transition-all',
                  petType === 'CAT' ? 'bg-orange-500 text-white' : 'bg-gray-100 text-gray-600'
                ]"
              >
                🐱 猫咪
              </button>
            </div>
          </div>

          <!-- 宠物名 -->
          <div class="mb-4">
            <label class="block text-xs font-bold text-gray-400 mb-2">宠物名字</label>
            <input 
              v-model="petName"
              type="text"
              placeholder="请输入宠物名字"
              class="w-full bg-white border-2 border-gray-200 rounded-xl py-3 px-4 text-gray-700 focus:outline-none focus:border-orange-400 transition-colors"
            />
          </div>

          <!-- 体重 -->
          <div class="mb-4">
            <label class="block text-xs font-bold text-gray-400 mb-2">体重 (kg)</label>
            <input 
              v-model.number="weight"
              type="number"
              placeholder="请输入体重"
              class="w-full bg-white border-2 border-gray-200 rounded-xl py-3 px-4 text-gray-700 focus:outline-none focus:border-orange-400 transition-colors"
            />
          </div>

          <!-- 品种 -->
          <div>
            <label class="block text-xs font-bold text-gray-400 mb-2">品种</label>
            <input 
              v-model="breed"
              type="text"
              placeholder="例如：金毛、英短"
              class="w-full bg-white border-2 border-gray-200 rounded-xl py-3 px-4 text-gray-700 focus:outline-none focus:border-orange-400 transition-colors"
            />
          </div>
        </div>

        <!-- 出行路线 -->
        <div class="bg-white rounded-2xl p-5 shadow-sm">
          <h3 class="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">✈️ 出行路线</h3>
          
          <!-- 出发地 -->
          <div class="mb-4">
            <label class="block text-xs font-bold text-gray-400 mb-2">出发地</label>
            <input 
              v-model="from"
              type="text"
              placeholder="例如：上海"
              class="w-full bg-white border-2 border-gray-200 rounded-xl py-3 px-4 text-gray-700 focus:outline-none focus:border-orange-400 transition-colors"
            />
          </div>

          <div class="mb-4">
            <label class="block text-xs font-bold text-gray-400 mb-2">目的地</label>
            <input 
              v-model="to"
              type="text"
              placeholder="例如：北京"
              class="w-full bg-white border-2 border-gray-200 rounded-xl py-3 px-4 text-gray-700 focus:outline-none focus:border-orange-400 transition-colors"
            />
          </div>

          <!-- 日期 -->
          <div class="mb-4">
            <label class="block text-xs font-bold text-gray-400 mb-2">出行日期</label>
            <input 
              v-model="startDate"
              type="date"
              class="w-full bg-white border-2 border-gray-200 rounded-xl py-3 px-4 text-gray-700 focus:outline-none focus:border-orange-400 transition-colors"
            />
          </div>

          <!-- 预算 -->
          <div>
            <label class="block text-xs font-bold text-gray-400 mb-2">预算 (元)</label>
            <input 
              v-model.number="offer"
              type="number"
              placeholder="请输入报酬"
              class="w-full bg-white border-2 border-gray-200 rounded-xl py-3 px-4 text-gray-700 focus:outline-none focus:border-orange-400 transition-colors"
            />
          </div>
        </div>

        <!-- 备注 -->
        <div class="bg-white rounded-2xl p-5 shadow-sm">
          <h3 class="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">📝 备注</h3>
          <textarea 
            v-model="message"
            placeholder="请输入其他要求或备注..."
            rows="3"
            class="w-full bg-white border-2 border-gray-200 rounded-xl py-3 px-4 text-gray-700 focus:outline-none focus:border-orange-400 transition-colors resize-none"
          ></textarea>
        </div>

        <!-- 提交按钮 -->
        <button 
          type="submit"
          class="w-full py-4 rounded-2xl font-bold text-white tracking-wider bg-gradient-to-br from-orange-400 to-amber-500 shadow-lg hover:scale-[1.02] active:scale-[0.98] transition-all"
        >
          发 布
        </button>

      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { taskApi, petApi } from '../router'

const petType = ref<'DOG' | 'CAT'>('DOG')
const petName = ref('')
const weight = ref<number>(0)
const breed = ref('')
const from = ref('')
const to = ref('')
const startDate = ref('')
const offer = ref<number>(0)
const message = ref('')

const handleSubmit = async () => {
  if (!from.value || !to.value || !startDate.value) {
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
    // 先创建宠物
    let petId = null
    if (petName.value) {
      const pet = await petApi.create({
        owner_id: user.id,
        pet_type: petType.value,
        name: petName.value,
        weight: weight.value,
        breed: breed.value
      })
      petId = pet.id
    }

    // 创建任务
    await taskApi.create({
      owner_id: user.id,
      pet_id: petId,
      from_city: from.value,
      to_city: to.value,
      travel_date: startDate.value,
      budget_min: offer.value,
      budget_max: offer.value,
      remark: message.value,
      status: 'OPEN'
    })

    alert('发布成功！')
    window.location.href = '/welcome'
  } catch (e) {
    console.error('发布失败:', e)
    alert('发布失败，请稍后重试')
  }
}
</script>
