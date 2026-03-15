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
        🔍 浏览任务
      </h1>

      <!-- 加载状态 -->
      <div v-if="loading" class="text-center py-12">
        <span class="text-gray-400">加载中...</span>
      </div>

      <template v-if="!loading">
        <!-- 筛选 -->
        <div class="flex gap-2 mb-4 overflow-x-auto pb-2">
          <button 
            @click="petFilter = 'ALL'"
            :class="[
              'px-4 py-2 rounded-full text-xs font-bold whitespace-nowrap transition-all',
              petFilter === 'ALL' ? 'bg-gray-800 text-white' : 'bg-white text-gray-500'
            ]"
          >
            全部
          </button>
          <button 
            @click="petFilter = 'DOG'"
            :class="[
              'px-4 py-2 rounded-full text-xs font-bold whitespace-nowrap transition-all',
              petFilter === 'DOG' ? 'bg-orange-500 text-white' : 'bg-white text-gray-500'
            ]"
          >
            🐕 狗狗
          </button>
          <button 
            @click="petFilter = 'CAT'"
            :class="[
              'px-4 py-2 rounded-full text-xs font-bold whitespace-nowrap transition-all',
              petFilter === 'CAT' ? 'bg-orange-500 text-white' : 'bg-white text-gray-500'
            ]"
          >
            🐱 猫咪
          </button>
        </div>

        <!-- 任务列表 -->
        <div class="space-y-4">
          <div 
            v-for="task in filteredTasks" 
            :key="task.id"
            @click="$router.push(`/apply-task/${task.id}`)"
            class="bg-white rounded-2xl p-5 shadow-[4px_4px_10px_rgba(0,0,0,0.05)] cursor-pointer hover:shadow-md transition-all"
          >
            <!-- 宠物类型标签 -->
            <div class="flex items-center gap-2 mb-3">
              <span class="px-2 py-1 bg-orange-100 text-orange-500 text-xs font-bold rounded-full">
                {{ task.pet_type === 'DOG' ? '🐕 狗狗' : '🐱 猫咪' }}
              </span>
            </div>

            <!-- 路线 -->
            <div class="flex items-center gap-2 mb-3">
              <span class="text-sm font-bold text-gray-700">{{ task.from_city }}</span>
              <span class="text-gray-400">→</span>
              <span class="text-sm font-bold text-gray-700">{{ task.to_city }}</span>
            </div>

            <!-- 日期和报酬 -->
            <div class="flex justify-between items-center">
              <span class="text-xs text-gray-400">📅 {{ task.travel_date }}</span>
              <span class="text-sm font-bold text-green-500">💰 {{ task.budget_min }}-{{ task.budget_max }}元</span>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-if="filteredTasks.length === 0" class="text-center py-12">
          <span class="text-4xl block mb-4">🔍</span>
          <p class="text-gray-400 text-sm">暂无匹配的任务</p>
        </div>
      </template>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { taskApi } from '../router'

interface Task {
  id: number
  pet_type: string
  from_city: string
  to_city: string
  travel_date: string
  budget_min: number
  budget_max: number
}

const loading = ref(true)
const petFilter = ref<'ALL' | 'DOG' | 'CAT'>('ALL')
const tasks = ref<Task[]>([])

const filteredTasks = computed(() => {
  if (petFilter.value === 'ALL') return tasks.value
  return tasks.value
})

onMounted(async () => {
  try {
    const data = await taskApi.getOpen()
    tasks.value = data
  } catch (e) {
    console.error('获取任务失败:', e)
  } finally {
    loading.value = false
  }
})
</script>
