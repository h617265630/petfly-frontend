<template>
  <div class="min-h-screen pb-16 bg-gradient-to-b from-amber-50 via-orange-50 to-pink-50 py-8 px-4">
    
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
      <h1 class="text-2xl font-bold text-center text-gray-700 mb-8">
        创建账户
      </h1>

      <!-- 角色选择 -->
      <div class="mb-8">
        <p class="text-sm text-gray-500 text-center mb-4">选择你的身份</p>
        <div class="flex gap-4 justify-center">
          <!-- Pet Owner -->
          <button 
            type="button"
            @click="role = 'OWNER'"
            :class="[
              'flex-1 py-4 rounded-2xl font-bold text-sm tracking-wide transition-all duration-300',
              role === 'OWNER' 
                ? 'bg-gradient-to-br from-orange-400 to-amber-500 text-white shadow-lg' 
                : 'bg-white text-gray-500 shadow'
            ]"
          >
            🐕 PET OWNER
          </button>
          
          <!-- Pet Nanny -->
          <button 
            type="button"
            @click="role = 'FLYER'"
            :class="[
              'flex-1 py-4 rounded-2xl font-bold text-sm tracking-wide transition-all duration-300',
              role === 'FLYER' 
                ? 'bg-gradient-to-br from-green-400 to-emerald-500 text-white shadow-lg' 
                : 'bg-white text-gray-500 shadow'
            ]"
          >
            ✈️ FLY NANNY
          </button>
        </div>
      </div>

      <!-- 注册表单 -->
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
            class="w-full bg-white border-2 border-gray-200 rounded-xl py-3 px-4 text-gray-700 focus:outline-none focus:border-orange-400 transition-colors"
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
            class="w-full bg-white border-2 border-gray-200 rounded-xl py-3 px-4 text-gray-700 focus:outline-none focus:border-orange-400 transition-colors"
          />
        </div>

        <!-- 确认密码 -->
        <div>
          <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">
            确认密码
          </label>
          <input 
            v-model="confirmPassword"
            type="password"
            required
            placeholder="请再次输入密码"
            class="w-full bg-white border-2 border-gray-200 rounded-xl py-3 px-4 text-gray-700 focus:outline-none focus:border-orange-400 transition-colors"
          />
        </div>

        <!-- 性别选择 -->
        <div v-if="role === 'OWNER'">
          <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">
            性别
          </label>
          <div class="flex gap-3">
            <button 
              type="button"
              v-for="g in genders" 
              :key="g.value"
              @click="gender = g.value"
              :class="[
                'flex-1 py-3 rounded-xl font-bold text-sm transition-all',
                gender === g.value
                  ? 'bg-orange-500 text-white'
                  : 'bg-gray-200 text-gray-600'
              ]"
            >
              {{ g.label }}
            </button>
          </div>
        </div>

        <!-- 提交按钮 -->
        <button 
          type="submit"
          class="w-full py-4 rounded-2xl font-bold text-white tracking-wider transition-all duration-300 hover:scale-[1.02] active:scale-[0.98]"
          :class="role === 'OWNER' 
            ? 'bg-gradient-to-br from-orange-400 to-amber-500 shadow-lg' 
            : 'bg-gradient-to-br from-green-400 to-emerald-500 shadow-lg'"
        >
          注 册
        </button>

      </form>

      <!-- 登录链接 -->
      <p class="text-center text-sm text-gray-400 mt-6">
        已有账户？ 
        <span 
          @click="goToLogin"
          class="text-orange-500 cursor-pointer hover:underline font-bold"
        >
          立即登录
        </span>
      </p>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { userApi } from '../router'

const role = ref<'OWNER' | 'FLYER'>('OWNER')
const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const gender = ref('Male')

const genders = [
  { label: '男生', value: 'Male' },
  { label: '女生', value: 'Female' },
  { label: '家庭', value: 'Family' }
]

// 验证用户名：最少6个字符
const validateUsername = (username: string): boolean => {
  if (username.length < 6) {
    alert('用户名需要至少6个字符')
    return false
  }
  return true
}

// 验证密码：必须包含英文字母和数字
const validatePassword = (password: string): boolean => {
  if (password.length < 6) {
    alert('密码需要至少6个字符')
    return false
  }
  const hasLetter = /[a-zA-Z]/.test(password)
  const hasNumber = /[0-9]/.test(password)
  if (!hasLetter || !hasNumber) {
    alert('密码必须包含英文字母和数字')
    return false
  }
  return true
}

const goToLogin = () => {
  if (role.value === 'OWNER') {
    window.location.href = '/owner/signin'
  } else {
    window.location.href = '/nanny/signin'
  }
}

const handleSubmit = async () => {
  // 验证用户名
  if (!validateUsername(username.value)) {
    return
  }
  
  // 验证密码
  if (!validatePassword(password.value)) {
    return
  }
  
  // 验证确认密码
  if (password.value !== confirmPassword.value) {
    alert('两次密码不一致')
    return
  }
  
  try {
    const user = await userApi.register({
      username: username.value,
      password: password.value,
      role: role.value,
      gender: gender.value,
      name: username.value,
      status: 1
    })
    
    alert('注册成功！')
    goToLogin()
  } catch (e: any) {
    console.error('注册失败:', e)
    alert('注册失败: ' + (e.message || '未知错误'))
  }
}
</script>
