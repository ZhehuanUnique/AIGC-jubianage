<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- 历史视频区域 -->
    <div class="mb-8">
      <!-- 筛选栏 -->
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-2xl font-bold text-gray-800">今天</h2>
        <div class="flex items-center gap-2">
          <!-- 时间筛选 -->
          <div class="relative">
            <button
              @click="showTimeFilter = !showTimeFilter"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2',
                filters.timeRange !== 'all' ? 'bg-primary-50 text-primary-600' : 'bg-white text-gray-700 hover:bg-gray-50'
              ]"
            >
              时间
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="showTimeFilter ? 'M5 15l7-7 7 7' : 'M19 9l-7 7-7-7'" />
              </svg>
            </button>
            <!-- 时间筛选下拉 -->
            <div
              v-if="showTimeFilter"
              class="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50 p-4"
            >
              <!-- 日期范围选择 -->
              <div class="mb-4 flex items-center gap-2">
                <input
                  v-model="filters.startDate"
                  type="date"
                  class="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm"
                  placeholder="开始日期"
                />
                <span class="text-gray-400">-</span>
                <input
                  v-model="filters.endDate"
                  type="date"
                  class="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm"
                  placeholder="结束日期"
                />
              </div>
              <!-- 预设选项 -->
              <div class="space-y-2">
                <button
                  v-for="option in timeOptions"
                  :key="option.value"
                  @click="selectTimeRange(option.value)"
                  :class="[
                    'w-full text-left px-3 py-2 rounded-lg text-sm transition-all flex items-center justify-between',
                    filters.timeRange === option.value ? 'bg-primary-50 text-primary-600' : 'hover:bg-gray-50'
                  ]"
                >
                  {{ option.label }}
                  <svg v-if="filters.timeRange === option.value" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- 视频类型筛选 -->
          <div class="relative">
            <button
              @click="showVideoFilter = !showVideoFilter"
              class="px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 bg-white text-gray-700 hover:bg-gray-50"
            >
              视频
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            <div
              v-if="showVideoFilter"
              class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-50 p-2"
            >
              <button
                v-for="option in videoTypeOptions"
                :key="option.value"
                @click="selectVideoType(option.value)"
                :class="[
                  'w-full text-left px-3 py-2 rounded-lg text-sm transition-all flex items-center justify-between',
                  filters.videoType === option.value ? 'bg-primary-50 text-primary-600' : 'hover:bg-gray-50'
                ]"
              >
                {{ option.label }}
                <svg v-if="filters.videoType === option.value" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </button>
            </div>
          </div>

          <!-- 操作类型筛选 -->
          <div class="relative">
            <button
              @click="showOperationFilter = !showOperationFilter"
              class="px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 bg-white text-gray-700 hover:bg-gray-50"
            >
              操作类型
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            <div
              v-if="showOperationFilter"
              class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-50 p-2"
            >
              <button
                v-for="option in operationTypeOptions"
                :key="option.value"
                @click="selectOperationType(option.value)"
                :class="[
                  'w-full text-left px-3 py-2 rounded-lg text-sm transition-all flex items-center justify-between',
                  filters.operationType === option.value ? 'bg-primary-50 text-primary-600' : 'hover:bg-gray-50'
                ]"
              >
                {{ option.label }}
                <svg v-if="filters.operationType === option.value" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

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

    <!-- 分隔线 -->
    <div class="border-t border-gray-200 my-8"></div>

    <!-- 视频生成区域 -->
    <div class="w-full">
      <!-- 标题 -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">
          开启你的<span class="text-primary-500">视频生成</span>
          <span class="text-primary-600">剧变时代</span>!
        </h1>
      </div>

      <!-- 主输入区域 -->
      <div class="bg-white rounded-2xl p-6 mb-6 shadow-sm">
        <!-- 输入框 -->
        <textarea
          v-model="prompt"
          placeholder="请描述你想生成的视频"
          class="w-full min-h-[120px] bg-transparent border-none outline-none resize-none text-gray-700 placeholder-gray-400 text-lg leading-relaxed"
          @input="handleInput"
        />

        <!-- 首尾帧上传卡片 -->
        <div class="flex items-center gap-4 mt-6">
          <!-- 首帧卡片 -->
          <div
            class="relative flex-1 cursor-pointer group"
            @mouseenter="hoveredFrame = 'first'"
            @mouseleave="hoveredFrame = null"
            @click="triggerFirstFrameUpload"
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
                'relative w-full h-48 bg-gray-50 border-2 border-dashed rounded-xl flex flex-col items-center justify-center transition-all duration-300',
                hoveredFrame === 'first' ? 'border-primary-500 shadow-lg transform -translate-y-2' : 'border-gray-300',
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
                <div class="w-12 h-12 bg-gray-200 rounded-lg flex items-center justify-center mb-3">
                  <svg class="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                </div>
                <span class="text-sm text-gray-600 font-medium">首帧</span>
              </div>
              <button
                v-if="firstFramePreview"
                @click.stop="clearFirstFrame"
                class="absolute top-2 right-2 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center text-xs hover:bg-red-600 z-20"
              >
                ×
              </button>
            </div>
          </div>

          <!-- 双向箭头 -->
          <div class="flex-shrink-0">
            <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
            </svg>
          </div>

          <!-- 尾帧卡片 -->
          <div
            class="relative flex-1 cursor-pointer group"
            @mouseenter="hoveredFrame = 'last'"
            @mouseleave="hoveredFrame = null"
            @click="triggerLastFrameUpload"
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
                'relative w-full h-48 bg-gray-50 border-2 border-dashed rounded-xl flex flex-col items-center justify-center transition-all duration-300',
                hoveredFrame === 'last' ? 'border-primary-500 shadow-lg transform -translate-y-2' : 'border-gray-300',
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
                <div class="w-12 h-12 bg-gray-200 rounded-lg flex items-center justify-center mb-3">
                  <svg class="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                </div>
                <span class="text-sm text-gray-600 font-medium">尾帧</span>
              </div>
              <button
                v-if="lastFramePreview"
                @click.stop="clearLastFrame"
                class="absolute top-2 right-2 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center text-xs hover:bg-red-600 z-20"
              >
                ×
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 控制栏 -->
      <div class="flex items-center justify-between bg-white rounded-xl p-4 shadow-sm">
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

      <!-- 错误提示 -->
      <div v-if="error || videoStore.error" class="mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
        <div class="flex items-start gap-3">
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useVideoStore } from '~/stores/video'
import { useHistoryStore } from '~/stores/history'

const config = useRuntimeConfig()
const videoStore = useVideoStore()
const historyStore = useHistoryStore()

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

// 筛选相关
const showTimeFilter = ref(false)
const showVideoFilter = ref(false)
const showOperationFilter = ref(false)
const filters = ref({
  timeRange: 'all' as 'all' | 'week' | 'month' | 'quarter' | 'custom',
  startDate: '',
  endDate: '',
  videoType: 'all' as 'all' | 'personal',
  operationType: 'all' as 'all' | 'ultra_hd' | 'favorite' | 'liked'
})

const timeOptions = [
  { label: '全部', value: 'all' },
  { label: '最近一周', value: 'week' },
  { label: '最近一个月', value: 'month' },
  { label: '最近三个月', value: 'quarter' }
]

const videoTypeOptions = [
  { label: '全部', value: 'all' },
  { label: '个人', value: 'personal' }
]

const operationTypeOptions = [
  { label: '全部', value: 'all' },
  { label: '已超清', value: 'ultra_hd' },
  { label: '收藏', value: 'favorite' },
  { label: '已点赞', value: 'liked' }
]

// 视频引用管理（用于hover播放）
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

// 筛选函数
const selectTimeRange = (value: string) => {
  filters.value.timeRange = value as any
  showTimeFilter.value = false
  applyFilters()
}

const selectVideoType = (value: string) => {
  filters.value.videoType = value as any
  showVideoFilter.value = false
  applyFilters()
}

const selectOperationType = (value: string) => {
  filters.value.operationType = value as any
  showOperationFilter.value = false
  applyFilters()
}

const applyFilters = () => {
  historyStore.setFilters(filters.value)
  historyStore.applyFilters(filters.value)
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

// 点击外部关闭筛选下拉
const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (!target.closest('.relative')) {
    showTimeFilter.value = false
    showVideoFilter.value = false
    showOperationFilter.value = false
  }
}

onMounted(() => {
  loadHistory()
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
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
