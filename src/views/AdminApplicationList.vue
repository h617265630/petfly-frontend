<template>
  <div class="min-h-screen pb-20">
    <div class="bg-gradient-to-br from-purple-400 to-pink-500 text-white p-6">
      <h2 class="text-xl font-bold">📝 申请列表</h2>
    </div>

    <div class="p-4 space-y-3">
      <div v-for="app in applications" :key="app.id" class="bg-white rounded-2xl p-4 shadow-sm">
        <div class="flex justify-between items-start mb-2">
          <div>
            <p class="font-bold text-gray-800">{{ app.from_city }} → {{ app.to_city }}</p>
            <p class="text-sm text-gray-400">{{ app.travel_date }}</p>
          </div>
          <span :class="{
            'bg-yellow-100 text-yellow-600': app.status === 'PENDING',
            'bg-blue-100 text-blue-600': app.status === 'SHORTLISTED',
            'bg-green-100 text-green-600': app.status === 'ACCEPTED',
            'bg-gray-100 text-gray-500': app.status === 'REJECTED'
          }" class="px-2 py-1 text-xs font-bold rounded-full">
            {{ app.status }}
          </span>
        </div>
        <p class="text-sm text-gray-500">Flyer ID: {{ app.flyer_id }} | 期望报酬: {{ app.expected_price }}元</p>
        <p class="text-sm text-gray-400 mt-1">{{ app.introduction }}</p>
      </div>
    </div>

    <div v-if="applications.length === 0" class="text-center py-12">
      <span class="text-5xl block">📝</span>
      <p class="text-gray-400">暂无申请</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { applicationApi } from '../router'

const applications = ref<any[]>([])

onMounted(async () => {
  applications.value = await applicationApi.getAll()
})
</script>
