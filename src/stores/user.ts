import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { userApi } from '../router'

export interface User {
  id: number
  phone: string
  country_code: string
  wechat?: string
  role: 'OWNER' | 'FLYER' | 'MANAGER'
  name?: string
  avatar?: string
}

export const useUserStore = defineStore('user', () => {
  const currentUser = ref<User | null>(null)
  const isLoggedIn = computed(() => !!currentUser.value)

  async function login(phone: string) {
    try {
      const user = await userApi.login(phone)
      if (user) {
        currentUser.value = user
        localStorage.setItem('petfly_user', JSON.stringify(user))
        return user
      }
      return null
    } catch (e) {
      console.error('登录失败:', e)
      return null
    }
  }

  async function register(userData: any) {
    try {
      const user = await userApi.register(userData)
      currentUser.value = user
      localStorage.setItem('petfly_user', JSON.stringify(user))
      return user
    } catch (e) {
      console.error('注册失败:', e)
      return null
    }
  }

  function logout() {
    currentUser.value = null
    localStorage.removeItem('petfly_user')
  }

  function restoreSession() {
    const saved = localStorage.getItem('petfly_user')
    if (saved) {
      try {
        currentUser.value = JSON.parse(saved)
      } catch (e) {
        localStorage.removeItem('petfly_user')
      }
    }
  }

  return { 
    currentUser, 
    isLoggedIn, 
    login, 
    register, 
    logout,
    restoreSession 
  }
})
