<template>
  <div class="min-h-screen pb-20">
    <div class="bg-gradient-to-br from-blue-400 to-indigo-500 text-white p-6">
      <h2 class="text-xl font-bold">📋 任务列表</h2>
    </div>

    <div class="p-4 space-y-3">
      <div v-for="task in tasks" :key="task.id" class="bg-white rounded-2xl p-4 shadow-sm">
        <div class="flex justify-between items-start mb-2">
          <div>
            <p class="font-bold text-gray-800">{{ task.from_city }} → {{ task.to_city }}</p>
            <p class="text-sm text-gray-400">{{ task.travel_date }}</p>
          </div>
          <span :class="{
            'bg-gray-100 text-gray-500': task.status === 'DRAFT',
            'bg-yellow-100 text-yellow-600': task.status === 'PENDING',
            'bg-green-100 text-green-600': task.status === 'OPEN',
            'bg-blue-100 text-blue-600': task.status === 'SELECTING',
            'bg-purple-100 text-purple-600': task.status === 'CONFIRMED',
            'bg-red-100 text-red-600': task.status === 'CANCELLED'
          }" class="px-2 py-1 text-xs font-bold rounded-full">
            {{ task.status }}
          </span>
        </div>
        <p class="text-sm text-gray-500">预算: {{ task.budget_min }}-{{ task.budget_max }}元</p>
      </div>
    </div>

    <div v-if="tasks.length === 0" class="text-center py-12">
      <span class="text-5xl block">📋</span>
      <p class="text-gray-400">暂无任务</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { taskApi } from '../router'

const tasks = ref<any[]>([])

onMounted(async () => {
  tasks.value = await taskApi.getAll()
})
</script>
