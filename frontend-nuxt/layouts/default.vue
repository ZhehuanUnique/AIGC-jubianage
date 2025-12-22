<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 导航栏 -->
    <nav class="bg-white border-b border-gray-200 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Logo/标题 -->
          <div class="flex items-center">
            <h1 class="text-xl font-bold text-gray-800">
              剧变时代
            </h1>
          </div>

          <!-- 导航标签 -->
          <div class="flex items-center space-x-1">
            <NuxtLink
              to="/"
              class="px-4 py-2 rounded-lg text-sm font-medium transition-all"
              :class="isActive('/') ? 'bg-primary-50 text-primary-600' : 'text-gray-600 hover:bg-gray-100'"
            >
              视频生成
            </NuxtLink>
            <NuxtLink
              to="/assets"
              class="px-4 py-2 rounded-lg text-sm font-medium transition-all"
              :class="isActive('/assets') ? 'bg-primary-50 text-primary-600' : 'text-gray-600 hover:bg-gray-100'"
            >
              资产管理
            </NuxtLink>
            <NuxtLink
              to="/knowledge"
              class="px-4 py-2 rounded-lg text-sm font-medium transition-all"
              :class="isActive('/knowledge') ? 'bg-primary-50 text-primary-600' : 'text-gray-600 hover:bg-gray-100'"
            >
              知识库
            </NuxtLink>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主内容区域 -->
    <main>
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()

const isActive = (path: string) => {
  if (path === '/') {
    return route.path === '/'
  }
  return route.path.startsWith(path)
}
</script>

