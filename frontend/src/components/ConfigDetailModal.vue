<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center overflow-x-hidden overflow-y-auto outline-none focus:outline-none py-4">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-black opacity-50" @click="$emit('close')"></div>

    <!-- Modal -->
    <div class="relative w-full max-w-5xl mx-4 bg-white rounded-lg shadow-lg flex flex-col max-h-[calc(100vh-2rem)]">
      <!-- Header -->
      <div class="flex items-start justify-between p-4 border-b border-gray-200 rounded-t">
        <div>
          <h3 class="text-xl font-semibold text-gray-900">{{ config?.name }}</h3>
          <p class="mt-1 text-sm text-gray-500">Config ID: {{ config?.id }}</p>
        </div>
        <button
          @click="$emit('close')"
          class="p-1 ml-auto border-0 text-black opacity-50 float-right text-3xl leading-none font-semibold outline-none focus:outline-none hover:opacity-75"
        >
          <span class="block outline-none focus:outline-none">×</span>
        </button>
      </div>

      <!-- Body -->
      <div class="relative p-4 flex-auto overflow-y-auto">
        <div v-if="loading" class="flex flex-col items-center justify-center py-12">
          <svg class="w-8 h-8 mb-4 text-blue-500 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span class="text-gray-600">Loading configuration details...</span>
        </div>

        <div v-else-if="error" class="p-4 text-red-600 bg-red-50 rounded">
          {{ error }}
        </div>

        <div v-else class="space-y-4">
          <!-- Metadata - Compact Row Layout -->
          <div class="grid grid-cols-4 items-center text-sm">
            <div class="flex items-baseline gap-2">
              <span class="font-medium text-gray-500">Created:</span>
              <span class="text-gray-900">{{ formatDate(configDetail?.created_at) }}</span>
            </div>
            <div class="flex items-baseline gap-2">
              <span class="font-medium text-gray-500">Modified:</span>
              <span class="text-gray-900">{{ formatDate(configDetail?.modified_at) }}</span>
            </div>
            <div class="flex items-baseline gap-2">
              <span class="font-medium text-gray-500">Last Version:</span>
              <span class="text-gray-900">{{ configDetail?.last_used_with_version || 'Never' }}</span>
            </div>
            <div class="flex items-baseline gap-2">
              <span class="font-medium text-gray-500">Size:</span>
              <span class="text-gray-900">{{ formatSize(configDetail?.content?.length || 0) }}</span>
            </div>
          </div>

          <!-- Config Content -->
          <div>
            <div class="flex items-center justify-between mb-2">
              <h4 class="text-base font-medium text-gray-900">Configuration Content</h4>
              <button
                @click="copyContent"
                class="px-3 py-1 text-sm text-white transition-colors duration-200 bg-blue-500 rounded hover:bg-blue-600"
              >
                {{ copied ? 'Copied!' : 'Copy' }}
              </button>
            </div>
            <div class="relative">
              <pre class="p-3 overflow-x-auto text-sm text-green-400 bg-slate-900 rounded border border-slate-700 max-h-[45vh]"><code>{{ formattedContent }}</code></pre>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="flex items-center justify-end p-3 border-t border-gray-200 rounded-b">
        <button
          @click="$emit('close')"
          class="px-4 py-2 text-white transition-colors duration-200 bg-gray-500 rounded hover:bg-gray-600"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import api from '../services/api'

export interface Config {
  id: number
  name: string
  last_used_with_version: string | null
  created_at: string
  modified_at: string | null
}

interface ConfigDetail extends Config {
  content: string
}

const props = defineProps<{
  show: boolean
  config: Config | null
}>()

defineEmits<{
  (e: 'close'): void
}>()

const loading = ref(false)
const error = ref('')
const configDetail = ref<ConfigDetail | null>(null)
const copied = ref(false)

const formattedContent = computed(() => {
  if (!configDetail.value?.content) return ''
  try {
    const parsed = JSON.parse(configDetail.value.content)
    return JSON.stringify(parsed, null, 2)
  } catch {
    return configDetail.value.content
  }
})

const formatDate = (dateStr: string | null | undefined) => {
  if (!dateStr) return 'Never'
  return new Date(dateStr).toLocaleString()
}

const formatSize = (bytes: number) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const copyContent = async () => {
  try {
    await navigator.clipboard.writeText(formattedContent.value)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy content:', err)
  }
}

const fetchConfigDetail = async () => {
  if (!props.config) return

  loading.value = true
  error.value = ''

  try {
    const response = await api.get(`/1/configs/${props.config.id}`)
    configDetail.value = response.data
  } catch (err: any) {
    error.value = 'Failed to load configuration details'
    console.error('Failed to load config detail:', err)
  } finally {
    loading.value = false
  }
}

watch(() => props.show, (newShow) => {
  if (newShow) {
    fetchConfigDetail()
  } else {
    configDetail.value = null
    error.value = ''
  }
}, { immediate: true })
</script>
