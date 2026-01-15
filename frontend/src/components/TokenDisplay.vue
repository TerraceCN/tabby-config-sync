<template>
  <div class="p-6 mb-8 bg-white rounded shadow-md">
    <h2 class="mb-4 text-xl font-semibold text-gray-700">Config Sync Token</h2>
    
    <div v-if="loading" class="animate-pulse flex space-x-4">
      <div class="flex-1 h-10 bg-gray-200 rounded"></div>
      <div class="w-24 h-10 bg-gray-200 rounded"></div>
    </div>

    <div v-else class="flex items-center space-x-4">
      <div class="relative flex-1">
        <input 
          type="text" 
          :value="showToken ? token : '•'.repeat(32)" 
          readonly
          autocomplete="off"
          name="config_sync_token_display"
          class="w-full px-4 py-2 pr-20 text-gray-700 bg-gray-100 border rounded focus:outline-none focus:bg-white font-mono"
        >
        <button 
          @click="showToken = !showToken"
          class="absolute text-gray-500 transform -translate-y-1/2 right-10 top-1/2 hover:text-gray-700 focus:outline-none"
          title="Toggle visibility"
        >
          <!-- Eye Icon -->
          <svg v-if="!showToken" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
          <!-- Eye Off Icon -->
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.542-7a10.059 10.059 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.542 7a10.059 10.059 0 01-1.563 3.029m-5.858-.908a3 3 0 11-4.243-4.243m4.242 4.242L21 21" />
          </svg>
        </button>
        <button 
          @click="copyToken"
          class="absolute text-gray-500 transform -translate-y-1/2 right-2 top-1/2 hover:text-gray-700 focus:outline-none"
          title="Copy to clipboard"
        >
          <svg v-if="copied" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
        </button>
      </div>
      <button 
        @click="refreshToken" 
        class="flex items-center px-4 py-2 text-white transition-colors duration-200 bg-blue-500 rounded hover:bg-blue-600 focus:outline-none"
        :class="{ 'opacity-50 cursor-not-allowed': refreshing }"
        :disabled="refreshing"
        title="Refresh Token"
      >
        <svg v-if="!refreshing" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <svg v-else class="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        {{ refreshing ? 'Refreshing...' : 'Refresh' }}
      </button>
    </div>

    <!-- Confirmation Modal -->
    <div v-if="showRefreshConfirm" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div class="w-full max-w-sm p-6 mx-4 bg-white rounded shadow-lg">
        <h3 class="mb-4 text-lg font-bold text-gray-800">Confirm Refresh</h3>
        <p class="mb-6 text-gray-600">Are you sure you want to refresh the token? The old token will be invalid.</p>
        <div class="flex justify-end space-x-4">
          <button @click="showRefreshConfirm = false" class="px-4 py-2 text-gray-600 transition-colors hover:text-gray-800">Cancel</button>
          <button @click="performRefresh" class="px-4 py-2 text-white transition-colors bg-blue-500 rounded hover:bg-blue-600">Confirm</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '../services/api'

const props = defineProps<{
  token?: string
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'update:token', token: string): void
}>()

const showToken = ref(false)
const copied = ref(false)
const showRefreshConfirm = ref(false)
const refreshing = ref(false)

const copyToken = async () => {
  if (props.token) {
    try {
      await navigator.clipboard.writeText(props.token)
      copied.value = true
      setTimeout(() => {
        copied.value = false
      }, 2000)
    } catch (err) {
      console.error('Failed to copy: ', err)
      alert('Failed to copy token')
    }
  }
}

const refreshToken = () => {
  showRefreshConfirm.value = true
}

const performRefresh = async () => {
  showRefreshConfirm.value = false
  refreshing.value = true
  try {
    const response = await api.get('/1/user/refresh_config_sync_token')
    emit('update:token', response.data.config_sync_token)
  } catch (err: any) {
    alert('Failed to refresh token')
  } finally {
    refreshing.value = false
  }
}
</script>
