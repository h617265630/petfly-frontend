<template>
  <div class="min-h-screen pb-20">
    <div class="bg-gradient-to-br from-green-400 to-emerald-500 text-white p-6">
      <h2 class="text-xl font-bold">✈️ 陪飞员列表</h2>
    </div>

    <div class="p-4 space-y-3">
      <div v-for="user in users" :key="user.id" class="bg-white rounded-2xl p-4 shadow-sm">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center text-xl">✈️</div>
          <div class="flex-1">
            <p class="font-bold text-gray-800">{{ user.name }}</p>
            <p class="text-xs text-gray-400">{{ user.phone }}</p>
          </div>
          <span class="text-green-500 text-sm">✓</span>
        </div>
      </div>
    </div>

    <div v-if="users.length === 0" class="text-center py-12">
      <span class="text-5xl block">✈️</span>
      <p class="text-gray-400">暂无陪飞员</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { userApi } from '../router'

const users = ref<any[]>([])

onMounted(async () => {
  const all = await userApi.getAll()
  users.value = all.filter((u: any) => u.role === 'FLYER')
})
</script>
