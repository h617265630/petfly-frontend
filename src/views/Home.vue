<template>
  <div class="relative flex flex-col items-center justify-between min-h-screen pb-16 bg-gradient-to-b from-amber-50 via-orange-50 to-pink-50 overflow-hidden py-16">
    
    <!-- 背景装饰点 -->
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute top-[10%] left-[10%] w-2 h-2 bg-orange-200 rounded-full opacity-60"></div>
      <div class="absolute top-[5%] right-[20%] w-1.5 h-1.5 bg-amber-200 rounded-full opacity-50"></div>
      <div class="absolute top-[20%] left-[30%] w-1 h-1 bg-pink-200 rounded-full opacity-40"></div>
      <div class="absolute top-[15%] right-[10%] w-2 h-2 bg-orange-100 rounded-full opacity-50"></div>
      <div class="absolute bottom-[30%] left-[10%] w-1.5 h-1.5 bg-amber-200 rounded-full opacity-50"></div>
      <div class="absolute bottom-[10%] right-[15%] w-2 h-2 bg-pink-100 rounded-full opacity-40"></div>
      <div class="absolute top-[40%] left-[5%] w-1 h-1 bg-orange-300 rounded-full opacity-30"></div>
      <div class="absolute top-[50%] right-[5%] w-1.5 h-1.5 bg-amber-200 rounded-full opacity-40"></div>
      <div class="absolute bottom-[40%] left-[20%] w-1 h-1 bg-pink-200 rounded-full opacity-40"></div>
    </div>

    <!-- 顶部标题区 -->
    <div class="flex flex-col items-center z-10 w-full mt-10 space-y-8">
      <h1 class="text-5xl md:text-6xl font-extrabold text-gray-700 tracking-wide relative flex items-baseline justify-center">
        <!-- PET - 带猫耳朵 -->
        <span class="inline-flex items-baseline transform -rotate-3 origin-bottom-right">
          <span class="text-orange-500">P</span>
          <span class="relative mx-1 text-orange-500">
            E
            <svg class="absolute -top-3 left-0 w-full h-5 text-orange-500" viewBox="0 0 100 40" preserveAspectRatio="none" fill="currentColor">
              <path d="M20,40 L35,5 L50,40 Z" />
              <path d="M50,40 L65,5 L80,40 Z" />
            </svg>
          </span>
          <span class="text-orange-500">T</span>
        </span>

        <span class="w-6"></span>

        <!-- MATCH -->
        <span class="inline-flex items-baseline transform rotate-3 origin-bottom-left text-green-500">
          <span>M</span>
          <span>A</span>
          <span>T</span>
          <span>C</span>
          <span>H</span>
        </span>
      </h1>
      
      <p class="text-gray-400 text-lg font-bold tracking-wide">
        Find your perfect fly nanny
      </p>
    </div>

    <!-- 中间按钮区 -->
    <div class="flex flex-col items-center gap-10 w-full z-10 flex-1 justify-center -mt-6">
      <span class="text-lg font-bold text-gray-600 tracking-widest uppercase">I'M</span>
      
      <div class="flex items-center gap-10">
        <!-- Pet Owner - Claymorphism 圆形按钮 -->
        <button 
          @click="$router.push('/owner/signin')"
          class="w-36 h-36 rounded-full border-[3px] border-orange-400 flex flex-col items-center justify-center bg-gradient-to-br from-white to-orange-100 shadow-[8px_8px_16px_rgba(245,158,11,0.2),_-8px_-8px_16px_rgba(255,255,255,0.8)] hover:shadow-[12px_12px_20px_rgba(245,158,11,0.3),_-10px_-10px_20px_rgba(255,255,255,0.9)] transition-all duration-300 hover:scale-105 active:scale-95 group"
        >
          <span class="text-4xl mb-1 group-hover:scale-110 transition-transform">🐕</span>
          <span class="text-orange-500 font-extrabold text-xl tracking-wide">PET</span>
          <span class="text-orange-500 font-extrabold text-xl tracking-wide">OWNER</span>
        </button>

        <!-- Fly Nanny - Claymorphism 圆形按钮 -->
        <button 
          @click="$router.push('/nanny/signin')"
          class="w-36 h-36 rounded-full border-[3px] border-green-400 flex flex-col items-center justify-center bg-gradient-to-br from-white to-green-100 shadow-[8px_8px_16px_rgba(16,185,129,0.2),_-8px_-8px_16px_rgba(255,255,255,0.8)] hover:shadow-[12px_12px_20px_rgba(16,185,129,0.3),_-10px_-10px_20px_rgba(255,255,255,0.9)] transition-all duration-300 hover:scale-105 active:scale-95 group"
        >
          <span class="text-4xl mb-1 group-hover:scale-110 transition-transform">✈️</span>
          <span class="text-green-500 font-extrabold text-xl tracking-wide">FLY</span>
          <span class="text-green-500 font-extrabold text-xl tracking-wide">NANNY</span>
        </button>
      </div>
    </div>

    <!-- 底部链接区 -->
    <div class="z-10 flex flex-col items-center gap-8 mb-4">
      <!-- Square 入口 -->
      <div class="flex flex-col items-center gap-2 group cursor-pointer" @click="$router.push('/square')">
        <span class="text-gray-500 font-extrabold text-2xl tracking-[0.2em] uppercase group-hover:text-orange-500 transition-colors">
          SQUARE
        </span>
        <div class="w-24 h-[3px] bg-gray-400 group-hover:bg-orange-500 transition-colors"></div>
      </div>

      <!-- Footer -->
      <div class="flex items-center gap-3 text-[10px] text-gray-300 font-bold uppercase tracking-widest">
        <span class="hover:text-gray-500 cursor-pointer transition-colors">Terms of Service</span>
        <span class="text-gray-200">|</span>
        <span 
          @click="$router.push('/admin/signin')" 
          class="hover:text-gray-500 cursor-pointer transition-colors"
        >
          Admin Manage
        </span>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
</script>
