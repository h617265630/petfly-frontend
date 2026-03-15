<template>
  <div class="min-h-screen pb-16 bg-gradient-to-b from-green-50 via-emerald-50 to-teal-50 py-8 px-4">
    
    <!-- 返回首页 -->
    <div class="max-w-md mx-auto mb-6">
      <button 
        @click="$router.push('/')" 
        class="text-gray-400 hover:text-gray-600 transition-colors"
      >
        ← 返回
      </button>
    </div>

    <div class="max-w-md mx-auto">
      <!-- 标题 -->
      <div class="text-center mb-8">
        <span class="text-5xl mb-4 block">✈️</span>
        <h1 class="text-2xl font-bold text-gray-700">
          FLY NANNY 登录
        </h1>
      </div>

      <!-- 登录表单 -->
      <form @submit.prevent="handleSubmit" class="space-y-5">
        
        <!-- 用户名 -->
        <div>
          <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">
            用户名
          </label>
          <input 
            v-model="username"
            type="text"
            required
            placeholder="请输入用户名"
            class="w-full bg-white border-2 border-gray-200 rounded-xl py-3 px-4 text-gray-700 focus:outline-none focus:border-green-400 transition-colors"
          />
        </div>

        <!-- 密码 -->
        <div>
          <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">
            密码
          </label>
          <input 
            v-model="password"
            type="password"
            required
            placeholder="请输入密码"
            class="w-full bg-white border-2 border-gray-200 rounded-xl py-3 px-4 text-gray-700 focus:outline-none focus:border-green-400 transition-colors"
          />
        </div>

        <!-- 提交按钮 -->
        <button 
          type="submit"
          class="w-full py-4 rounded-2xl font-bold text-white tracking-wider transition-all duration-300 hover:scale-[1.02] active:scale-[0.98] bg-gradient-to-br from-green-400 to-emerald-500 shadow-lg"
        >
          登 录
        </button>

      </form>

      <!-- 注册链接 -->
      <p class="text-center text-sm text-gray-400 mt-6">
        还没有账户？ 
        <span 
          @click="window.location.href = '/register'"
          class="text-green-500 cursor-pointer hover:underline font-bold"
        >
          立即注册
        </span>
      </p>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { userApi } from '../router'

const username = ref('')
const password = ref('')
const window = globalThis.window

// 检查是否已登录
onMounted(() => {
  // 清除旧的可能错误的缓存
  const savedUser = localStorage.getItem('petfly_user')
  if (savedUser) {
    try {
      const user = JSON.parse(savedUser)
      // 如果已经是 Flyer，直接跳转
      if (user.role === 'FLYER') {
        window.location.href = '/browse-task'
      } else {
        // 否则清除缓存
        localStorage.removeItem('petfly_user')
      }
    } catch (e) {
      localStorage.removeItem('petfly_user')
    }
  }
})

const handleSubmit = async () => {
  if (!username.value || !password.value) {
    alert('请填写用户名和密码')
    return
  }
  
  try {
    const user = await userApi.loginByUsername(username.value, password.value)
    console.log('API返回:', user)
    
    if (user) {
      console.log('用户角色:', user.role)
      
      // 严格检查角色
      const userRole = String(user.role).trim().toUpperCase()
      
      if (userRole !== 'FLYER') {
        alert('错误：您的账户角色是 ' + user.role + '，不是 FLYER')
        return
      }
      
      localStorage.setItem('petfly_user', JSON.stringify(user))
      alert('登录成功！')
      window.location.href = '/browse-task'
    } else {
      alert('用户名或密码错误')
    }
  } catch (e) {
    console.error('登录错误:', e)
    alert('登录失败，请检查用户名和密码')
  }
}
</script>
