<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
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
              <!-- 已上传图片预览 -->
              <img
                v-if="firstFramePreview"
                :src="firstFramePreview"
                alt="首帧"
                class="absolute inset-0 w-full h-full object-cover rounded-xl"
              />
              <!-- 加号和文字 -->
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
              <!-- 删除按钮 -->
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
              <!-- 已上传图片预览 -->
              <img
                v-if="lastFramePreview"
                :src="lastFramePreview"
                alt="尾帧"
                class="absolute inset-0 w-full h-full object-cover rounded-xl"
              />
              <!-- 加号和文字 -->
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
              <!-- 删除按钮 -->
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
        <!-- 左侧控制 -->
        <div class="flex items-center gap-4">
          <!-- 视频生成下拉 -->
          <button class="flex items-center gap-2 text-primary-500 font-medium hover:text-primary-600">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
            视频生成
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          <!-- 时长选择 -->
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

        <!-- 右侧：生成按钮 -->
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

      <!-- 生成结果 -->
      <div v-if="generatedVideo || videoStore.isGenerating" class="mt-6 bg-white rounded-xl p-6 shadow-sm">
        <h3 class="text-lg font-semibold mb-4">生成结果</h3>
        <div v-if="generatedVideo?.video_url" class="space-y-4">
          <video
            :src="generatedVideo.video_url"
            controls
            class="w-full rounded-lg"
          />
          <div class="flex items-center justify-between text-sm text-gray-600">
            <span>任务 ID: {{ generatedVideo.task_id }}</span>
            <button
              @click="downloadVideo"
              class="text-primary-500 hover:text-primary-600 font-medium"
            >
              下载视频
            </button>
          </div>
        </div>
        <div v-else class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mb-4"></div>
          <p class="text-gray-500 text-lg">
            {{ generatedVideo?.status === 'processing' || videoStore.isGenerating 
              ? '视频生成中，请稍候...' 
              : '等待生成' }}
          </p>
          <p v-if="generatedVideo?.task_id" class="text-sm text-gray-400 mt-2">
            任务 ID: {{ generatedVideo.task_id }}
          </p>
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
            <p v-if="(error || videoStore.error)?.includes('无法连接')" class="text-red-600 text-xs mt-2">
              💡 提示：Render 免费实例在空闲时会休眠，首次请求可能需要等待 50 秒左右唤醒服务。
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useVideoStore } from '~/stores/video'

const config = useRuntimeConfig()
const videoStore = useVideoStore()

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

const generatedVideo = computed(() => videoStore.currentVideo)

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
  console.log('生成视频按钮被点击')
  
  // 验证输入
  if (!prompt.value.trim()) {
    error.value = '请输入视频描述'
    return
  }

  console.log('开始生成视频:', {
    prompt: prompt.value,
    duration: duration.value,
    hasFirstFrame: !!firstFrame.value,
    hasLastFrame: !!lastFrame.value
  })

  isGenerating.value = true
  error.value = ''

  try {
    // 处理首尾帧图片
    let firstFrameBase64 = null
    let lastFrameBase64 = null

    if (firstFrame.value) {
      firstFrameBase64 = await fileToBase64(firstFrame.value)
    }
    if (lastFrame.value) {
      lastFrameBase64 = await fileToBase64(lastFrame.value)
    }

    // 调用视频生成
    await videoStore.generateVideo({
      prompt: prompt.value.trim(),
      duration: duration.value,
      firstFrame: firstFrameBase64,
      lastFrame: lastFrameBase64,
      backendUrl: config.public.backendUrl
    })
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
      // 移除 data:image/...;base64, 前缀
      const base64 = result.split(',')[1]
      resolve(base64)
    }
    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}

const downloadVideo = () => {
  if (generatedVideo.value?.video_url) {
    const link = document.createElement('a')
    link.href = generatedVideo.value.video_url
    link.download = `video-${generatedVideo.value.task_id}.mp4`
    link.click()
  }
}
</script>

