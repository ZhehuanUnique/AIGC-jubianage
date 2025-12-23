<template>
  <div class="relative min-h-screen bg-gray-50">
    <!-- 历史视频区域（全屏滚动） -->
    <div class="pb-96 pt-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- 日期标题 -->
        <h2 class="text-2xl font-bold text-gray-800 mb-6">今天</h2>

        <!-- 历史视频网格 -->
        <div v-if="historyStore.loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
          <p class="text-gray-500 mt-4">加载中...</p>
        </div>
        <div v-else-if="historyStore.videos.length === 0" class="text-center py-12">
          <p class="text-gray-500">暂无历史视频</p>
        </div>
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          <div
            v-for="video in historyStore.videos"
            :key="video.id"
            class="group relative bg-white rounded-xl overflow-hidden shadow-sm hover:shadow-lg transition-all"
            @mouseenter="handleVideoHover(video.id, true)"
            @mouseleave="handleVideoHover(video.id, false)"
          >
            <!-- 视频容器 -->
            <div class="relative aspect-video bg-gray-100">
              <video
                :ref="el => setVideoRef(video.id, el)"
                :src="video.video_url"
                class="w-full h-full object-cover"
                muted
                loop
                preload="metadata"
              />
              <!-- 状态覆盖层 -->
              <div v-if="video.status !== 'completed'" class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                <div class="text-center text-white">
                  <div v-if="video.status === 'processing'" class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-white mb-2"></div>
                  <p class="text-sm">{{ getStatusText(video.status) }}</p>
                </div>
              </div>
              <!-- 操作按钮 -->
              <div class="absolute bottom-2 right-2 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  @click.stop="toggleFavorite(video.id)"
                  :class="[
                    'w-8 h-8 rounded-full bg-black bg-opacity-50 flex items-center justify-center text-white hover:bg-opacity-70',
                    video.is_favorite && 'bg-primary-500 bg-opacity-100'
                  ]"
                >
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
                  </svg>
                </button>
                <button
                  @click.stop="toggleLike(video.id)"
                  :class="[
                    'w-8 h-8 rounded-full bg-black bg-opacity-50 flex items-center justify-center text-white hover:bg-opacity-70',
                    video.is_liked && 'bg-red-500 bg-opacity-100'
                  ]"
                >
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
                  </svg>
                </button>
              </div>
            </div>
            <!-- 视频信息 -->
            <div class="p-3">
              <p class="text-sm text-gray-700 line-clamp-2 mb-2">{{ video.prompt }}</p>
              <div class="flex items-center justify-between text-xs text-gray-500">
                <span>视频 3.0 | {{ video.duration }}s</span>
                <span>{{ formatDate(video.created_at) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部边缘触发区域（用于检测鼠标靠近）- 始终存在，收缩时显示提示条 -->
    <div
      class="fixed bottom-0 left-0 right-0 z-50 transition-all duration-300"
      :class="isBottomBarCollapsed ? 'h-16' : 'h-4'"
      @mouseenter="handleBottomEdgeHover(true)"
      @mouseleave="handleBottomEdgeHover(false)"
      @click="isBottomBarCollapsed = false"
    >
      <!-- 收缩时显示提示条 -->
      <div v-if="isBottomBarCollapsed" class="h-full flex items-end">
        <div class="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-2">
          <div class="bg-white/90 backdrop-blur-sm rounded-t-2xl shadow-lg border-t border-x border-gray-200 px-4 py-2 cursor-pointer hover:bg-white transition-colors">
            <div class="flex items-center justify-center gap-2 text-xs text-gray-500 hover:text-primary-500 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
              </svg>
              <span>悬停或点击展开输入区域</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部悬浮输入区域 -->
    <div
      :class="[
        'fixed bottom-0 left-0 right-0 z-40 transition-all duration-300 ease-in-out',
        isBottomBarCollapsed ? 'translate-y-full opacity-0 pointer-events-none' : 'translate-y-0 opacity-100'
      ]"
      @mouseenter="handleBottomBarHover(true)"
      @mouseleave="handleBottomBarHover(false)"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="bg-white rounded-t-2xl shadow-lg border-t border-x border-gray-200 p-6">
          <!-- 完整内容 -->
          <div>
          <!-- 主要内容区域：首尾帧上传（左）和提示词输入（右） -->
          <div class="flex items-start gap-6 mb-4">
            <!-- 左侧：首尾帧上传块 -->
            <div class="flex-shrink-0 flex flex-col gap-3">
              <!-- 首帧卡片 -->
              <div
                class="relative cursor-pointer group"
                @mouseenter="hoveredFrame = 'first'"
                @mouseleave="hoveredFrame = null"
                @click.stop="triggerFirstFrameUpload"
              >
                <input
                  type="file"
                  accept="image/*"
                  @change="handleFirstFrame"
                  class="hidden"
                  ref="firstFrameInput"
                />
                <div
                  :class="[
                    'relative w-32 h-32 bg-gray-50 border-2 border-dashed rounded-xl flex flex-col items-center justify-center transition-all duration-300',
                    hoveredFrame === 'first' ? 'border-primary-500 shadow-lg transform scale-105' : 'border-gray-300',
                    firstFramePreview ? 'border-primary-500 bg-white' : ''
                  ]"
                >
                  <img
                    v-if="firstFramePreview"
                    :src="firstFramePreview"
                    alt="首帧"
                    class="absolute inset-0 w-full h-full object-cover rounded-xl"
                  />
                  <div
                    v-if="!firstFramePreview"
                    class="flex flex-col items-center justify-center z-10"
                  >
                    <div class="w-16 h-16 bg-gray-200 rounded-lg flex items-center justify-center mb-2">
                      <svg class="w-8 h-8 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                      </svg>
                    </div>
                    <span class="text-sm text-gray-600 font-medium">首帧</span>
                  </div>
                  <button
                    v-if="firstFramePreview"
                    @click.stop="clearFirstFrame"
                    class="absolute top-1 right-1 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center text-xs hover:bg-red-600 z-20"
                  >
                    ×
                  </button>
                </div>
              </div>

              <!-- 等号连接符 -->
              <div class="flex items-center justify-center">
                <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                </svg>
              </div>

              <!-- 尾帧卡片 -->
              <div
                class="relative cursor-pointer group"
                @mouseenter="hoveredFrame = 'last'"
                @mouseleave="hoveredFrame = null"
                @click.stop="triggerLastFrameUpload"
              >
                <input
                  type="file"
                  accept="image/*"
                  @change="handleLastFrame"
                  class="hidden"
                  ref="lastFrameInput"
                />
                <div
                  :class="[
                    'relative w-32 h-32 bg-gray-50 border-2 border-dashed rounded-xl flex flex-col items-center justify-center transition-all duration-300',
                    hoveredFrame === 'last' ? 'border-primary-500 shadow-lg transform scale-105' : 'border-gray-300',
                    lastFramePreview ? 'border-primary-500 bg-white' : ''
                  ]"
                >
                  <img
                    v-if="lastFramePreview"
                    :src="lastFramePreview"
                    alt="尾帧"
                    class="absolute inset-0 w-full h-full object-cover rounded-xl"
                  />
                  <div
                    v-if="!lastFramePreview"
                    class="flex flex-col items-center justify-center z-10"
                  >
                    <div class="w-16 h-16 bg-gray-200 rounded-lg flex items-center justify-center mb-2">
                      <svg class="w-8 h-8 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                      </svg>
                    </div>
                    <span class="text-sm text-gray-600 font-medium">尾帧</span>
                  </div>
                  <button
                    v-if="lastFramePreview"
                    @click.stop="clearLastFrame"
                    class="absolute top-1 right-1 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center text-xs hover:bg-red-600 z-20"
                  >
                    ×
                  </button>
                </div>
              </div>
            </div>

            <!-- 右侧：提示词输入框 -->
            <div class="flex-1">
              <textarea
                v-model="prompt"
                placeholder="输入文字,描述你想创作的画面内容、运动方式等。例如:一个3D形象的小男孩,在公园滑滑板。"
                :class="[
                  'w-full bg-transparent border-none outline-none resize-none text-gray-700 placeholder-gray-400 transition-all min-h-[200px] text-base leading-relaxed',
                  isInputFocused ? 'ring-2 ring-primary-500 rounded-lg' : ''
                ]"
                @input="handleInput"
                @focus="handleInputFocus"
                @blur="handleInputBlur"
              />
            </div>
          </div>

          <!-- 控制栏 -->
          <div class="flex items-center justify-between pt-4 border-t border-gray-200">
            <div class="flex items-center gap-4">
              <button class="flex items-center gap-2 text-primary-500 font-medium hover:text-primary-600">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                视频生成
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div class="flex items-center gap-2">
                <button
                  v-for="dur in durations"
                  :key="dur"
                  @click="duration = dur"
                  :class="[
                    'px-3 py-1.5 rounded-lg text-sm font-medium transition-all',
                    duration === dur
                      ? 'bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-sm'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  ]"
                >
                  {{ dur }}秒
                </button>
              </div>
            </div>
            <div class="flex items-center">
              <button
                type="button"
                @click="generateVideo"
                :disabled="!prompt.trim() || isGenerating || videoStore.isGenerating"
                :class="[
                  'px-6 py-3 bg-gradient-to-r from-primary-500 to-primary-600 text-white rounded-lg font-medium shadow-lg hover:shadow-xl hover:from-primary-600 hover:to-primary-700 active:scale-95 transition-all flex items-center gap-2',
                  (!prompt.trim() || isGenerating || videoStore.isGenerating) && 'opacity-50 cursor-not-allowed'
                ]"
              >
                <svg v-if="!isGenerating && !videoStore.isGenerating" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <svg v-else class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ (isGenerating || videoStore.isGenerating) ? '生成中...' : '生成视频' }}
              </button>
            </div>
          </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 错误提示 -->
    <div v-if="error || videoStore.error" class="fixed bottom-0 left-0 right-0 z-50 bg-red-50 border-t border-red-200 px-4 py-3">
      <div class="max-w-7xl mx-auto flex items-start gap-3">
        <svg class="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div class="flex-1">
          <p class="text-red-800 font-medium">请求失败</p>
          <p class="text-red-700 text-sm mt-1">{{ error || videoStore.error }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useVideoStore } from '~/stores/video'
import { useHistoryStore } from '~/stores/history'

const config = useRuntimeConfig()
const videoStore = useVideoStore()
const historyStore = useHistoryStore()

// 筛选相关（从布局组件同步）
const filters = ref({
  timeRange: 'all' as 'all' | 'week' | 'month' | 'quarter' | 'custom',
  startDate: '',
  endDate: '',
  videoType: 'all' as 'all' | 'personal',
  operationType: 'all' as 'all' | 'ultra_hd' | 'favorite' | 'liked'
})

// 监听筛选更新事件
const handleFiltersUpdated = (event: CustomEvent) => {
  filters.value = { ...event.detail }
  loadHistory()
}

// 视频生成相关
const prompt = ref('')
const duration = ref(5)
const durations = [5, 10]
const firstFrame = ref<File | null>(null)
const lastFrame = ref<File | null>(null)
const firstFramePreview = ref<string | null>(null)
const lastFramePreview = ref<string | null>(null)
const firstFrameInput = ref<HTMLInputElement | null>(null)
const lastFrameInput = ref<HTMLInputElement | null>(null)
const isGenerating = ref(false)
const error = ref('')
const hoveredFrame = ref<'first' | 'last' | null>(null)

// 悬浮窗口状态 - 默认收缩
const isBottomBarCollapsed = ref(true)
const isInputFocused = ref(false)
const isBottomEdgeHovered = ref(false)
const isBottomBarHovered = ref(false)
let scrollTimeout: NodeJS.Timeout | null = null
let bottomBarHoverTimeout: NodeJS.Timeout | null = null
let bottomEdgeHoverTimeout: NodeJS.Timeout | null = null

// 视频引用管理
const videoRefs = new Map<number, HTMLVideoElement | null>()

const setVideoRef = (videoId: number, el: HTMLVideoElement | null) => {
  if (el) {
    videoRefs.set(videoId, el)
  }
}

const handleVideoHover = (videoId: number, isHovering: boolean) => {
  const video = videoRefs.get(videoId)
  if (video) {
    if (isHovering) {
      video.play().catch(() => {})
    } else {
      video.pause()
      video.currentTime = 0
    }
  }
}

// 滚动处理
const handleScroll = () => {
  if (scrollTimeout) {
    clearTimeout(scrollTimeout)
  }
  
  scrollTimeout = setTimeout(() => {
    // 如果输入框有焦点或鼠标正在悬停，不自动收缩
    if (isInputFocused.value || isBottomBarHovered.value || isBottomEdgeHovered.value) {
      return
    }
    
    const scrollY = window.scrollY
    const windowHeight = window.innerHeight
    const documentHeight = document.documentElement.scrollHeight
    const distanceFromBottom = documentHeight - (scrollY + windowHeight)
    
    // 向上滚动时自动收缩
    // 如果不在底部附近（距离底部超过100px），则收缩
    if (distanceFromBottom > 100) {
      isBottomBarCollapsed.value = true
    } else {
      // 接近底部时展开
      isBottomBarCollapsed.value = false
    }
  }, 100)
}

// 底部边缘鼠标悬停（检测鼠标靠近底部）
const handleBottomEdgeHover = (isHovering: boolean) => {
  if (bottomEdgeHoverTimeout) {
    clearTimeout(bottomEdgeHoverTimeout)
  }
  
  isBottomEdgeHovered.value = isHovering
  
  if (isHovering) {
    // 鼠标靠近底部边缘时，立即展开悬浮窗口
    isBottomBarCollapsed.value = false
  } else {
    // 延迟检查是否需要收缩
    bottomEdgeHoverTimeout = setTimeout(() => {
      // 如果输入框没有焦点且鼠标不在悬浮窗口上，则收缩
      if (!isInputFocused.value && !isBottomBarHovered.value) {
        const scrollY = window.scrollY
        const windowHeight = window.innerHeight
        const documentHeight = document.documentElement.scrollHeight
        const distanceFromBottom = documentHeight - (scrollY + windowHeight)
        
        // 如果不在底部附近（超过100px），则收缩
        if (distanceFromBottom > 100) {
          isBottomBarCollapsed.value = true
        }
      }
    }, 300)
  }
}

// 底部悬浮栏鼠标悬停
const handleBottomBarHover = (isHovering: boolean) => {
  if (bottomBarHoverTimeout) {
    clearTimeout(bottomBarHoverTimeout)
  }
  
  isBottomBarHovered.value = isHovering
  
  if (isHovering) {
    // 鼠标悬停在悬浮窗口上时，保持展开
    isBottomBarCollapsed.value = false
  } else {
    // 延迟检查是否需要收缩
    bottomBarHoverTimeout = setTimeout(() => {
      // 如果输入框没有焦点且鼠标不在底部边缘，则收缩
      if (!isInputFocused.value && !isBottomEdgeHovered.value) {
        const scrollY = window.scrollY
        const windowHeight = window.innerHeight
        const documentHeight = document.documentElement.scrollHeight
        const distanceFromBottom = documentHeight - (scrollY + windowHeight)
        
        // 如果不在底部附近（超过100px），则收缩
        if (distanceFromBottom > 100) {
          isBottomBarCollapsed.value = true
        }
      }
    }, 300)
  }
}

// 输入框焦点处理
const handleInputFocus = () => {
  isInputFocused.value = true
  isBottomBarCollapsed.value = false
}

const handleInputBlur = () => {
  isInputFocused.value = false
  // 失去焦点后，如果不在底部附近且鼠标不在悬浮区域，则收缩
  setTimeout(() => {
    if (!isBottomBarHovered.value && !isBottomEdgeHovered.value) {
      const scrollY = window.scrollY
      const windowHeight = window.innerHeight
      const documentHeight = document.documentElement.scrollHeight
      const distanceFromBottom = documentHeight - (scrollY + windowHeight)
      
      if (distanceFromBottom > 100) {
        isBottomBarCollapsed.value = true
      }
    }
  }, 200)
}

// 加载历史记录
const loadHistory = async () => {
  try {
    await historyStore.fetchHistory({
      backendUrl: config.public.backendUrl,
      limit: 20,
      offset: 0,
      filters: filters.value
    })
  } catch (err: any) {
    console.error('加载历史记录失败:', err)
    // 如果是404错误，可能是API路径不对或后端未部署，静默处理
    if (err.status === 404 || err.statusCode === 404) {
      console.warn('历史记录API未找到，可能是后端未部署或路径配置错误')
    }
  }
}

// 视频生成相关函数
const handleInput = () => {
  error.value = ''
}

const triggerFirstFrameUpload = () => {
  firstFrameInput.value?.click()
}

const triggerLastFrameUpload = () => {
  lastFrameInput.value?.click()
}

const handleFirstFrame = async (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    firstFrame.value = target.files[0]
    firstFramePreview.value = await fileToDataURL(target.files[0])
  }
}

const handleLastFrame = async (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    lastFrame.value = target.files[0]
    lastFramePreview.value = await fileToDataURL(target.files[0])
  }
}

const clearFirstFrame = () => {
  firstFrame.value = null
  firstFramePreview.value = null
  if (firstFrameInput.value) {
    firstFrameInput.value.value = ''
  }
}

const clearLastFrame = () => {
  lastFrame.value = null
  lastFramePreview.value = null
  if (lastFrameInput.value) {
    lastFrameInput.value.value = ''
  }
}

const fileToDataURL = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result as string)
    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}

const generateVideo = async () => {
  if (!prompt.value.trim()) {
    error.value = '请输入视频描述'
    return
  }

  isGenerating.value = true
  error.value = ''

  try {
    let firstFrameBase64 = null
    let lastFrameBase64 = null

    if (firstFrame.value) {
      firstFrameBase64 = await fileToBase64(firstFrame.value)
    }
    if (lastFrame.value) {
      lastFrameBase64 = await fileToBase64(lastFrame.value)
    }

    await videoStore.generateVideo({
      prompt: prompt.value.trim(),
      duration: duration.value,
      firstFrame: firstFrameBase64,
      lastFrame: lastFrameBase64,
      backendUrl: config.public.backendUrl
    })

    // 生成成功后刷新历史记录
    await loadHistory()
    // 清空输入
    prompt.value = ''
    firstFrame.value = null
    lastFrame.value = null
    firstFramePreview.value = null
    lastFramePreview.value = null
  } catch (err: any) {
    console.error('生成视频失败:', err)
    error.value = err.message || '生成失败，请重试'
  } finally {
    isGenerating.value = false
  }
}

const fileToBase64 = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => {
      const result = reader.result as string
      const base64 = result.split(',')[1]
      resolve(base64)
    }
    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}

const toggleFavorite = async (videoId: number) => {
  await historyStore.toggleFavorite(videoId, config.public.backendUrl)
}

const toggleLike = async (videoId: number) => {
  await historyStore.toggleLike(videoId, config.public.backendUrl)
}

const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    pending: '等待中',
    processing: '生成中',
    completed: '已完成',
    failed: '生成失败'
  }
  return statusMap[status] || status
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' })
}

onMounted(() => {
  loadHistory()
  window.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('filters-updated', handleFiltersUpdated as EventListener)
  
  // 初始状态：默认收缩
  // 延迟检查，确保DOM已渲染
  setTimeout(() => {
    const scrollY = window.scrollY
    const windowHeight = window.innerHeight
    const documentHeight = document.documentElement.scrollHeight
    const distanceFromBottom = documentHeight - (scrollY + windowHeight)
    
    // 如果不在底部附近（超过100px），默认收缩
    // 否则保持展开（用户可能在底部）
    if (distanceFromBottom > 100) {
      isBottomBarCollapsed.value = true
    }
  }, 200)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('filters-updated', handleFiltersUpdated as EventListener)
  if (scrollTimeout) clearTimeout(scrollTimeout)
  if (bottomBarHoverTimeout) clearTimeout(bottomBarHoverTimeout)
  if (bottomEdgeHoverTimeout) clearTimeout(bottomEdgeHoverTimeout)
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
