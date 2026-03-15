<template>
  <div class="min-h-screen bg-gray-50">
    <div class="pb-14">
      <router-view />
    </div>
    <AppFooter 
      v-if="currentUser" 
      :role="currentUser.role" 
      :active="currentRoute" 
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from './stores/user'
import AppFooter from './components/AppFooter.vue'

const userStore = useUserStore()
const currentUser = computed(() => userStore.currentUser)
const currentRoute = ref('/browse-task')

onMounted(() => {
  // 恢复登录状态
  userStore.restoreSession()
  
  // 监听路由变化
  if (window.location.pathname) {
    currentRoute.value = window.location.pathname
  }
})
</script>
