<template>
  <div class="container px-4 py-8 mx-auto">
    <header class="flex items-center justify-between pb-4 mb-8 border-b border-gray-200">
      <h1 class="text-2xl font-bold text-gray-800">Dashboard</h1>
      <div class="flex items-center space-x-4">
        <button @click="openUserModal" class="text-gray-600 hover:text-gray-800 focus:outline-none">
          <span v-if="user" class="font-medium">{{ user.username }}</span>
          <span v-else>Profile</span>
        </button>
        <button @click="logout" class="px-4 py-2 text-white transition-colors duration-200 bg-red-500 rounded hover:bg-red-600">Logout</button>
      </div>
    </header>
    <main>
      <!-- Token Management Section -->
      <div v-if="user" class="p-6 mb-8 bg-white rounded shadow-md">
        <h2 class="mb-4 text-xl font-semibold text-gray-700">Config Sync Token</h2>
        <div class="flex items-center space-x-4">
          <div class="relative flex-1">
            <input 
              type="text" 
              :value="showToken ? user.config_sync_token : '•'.repeat(32)" 
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
            title="Refresh Token"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Refresh
          </button>
        </div>
      </div>
      <div v-if="loading" class="p-8 text-center text-gray-600">Loading...</div>
      <div v-else-if="error" class="p-8 text-center text-red-500">{{ error }}</div>
      <div v-else class="overflow-x-auto bg-white rounded shadow-md">
        <table class="min-w-full table-auto">
          <thead>
            <tr class="text-sm leading-normal text-gray-600 uppercase bg-gray-200">
              <th class="px-6 py-3 text-left">ID</th>
              <th class="px-6 py-3 text-left">Name</th>
              <th class="px-6 py-3 text-left">Created At</th>
              <th class="px-6 py-3 text-left">Modified At</th>
              <th class="px-6 py-3 text-left">Last Used Version</th>
              <th class="px-6 py-3 text-left">Actions</th>
            </tr>
          </thead>
          <tbody class="text-sm font-light text-gray-600">
            <tr v-for="config in configs" :key="config.id" class="border-b border-gray-200 hover:bg-gray-100">
              <td class="px-6 py-3 text-left whitespace-nowrap">{{ config.id }}</td>
              <td class="px-6 py-3 text-left whitespace-nowrap">{{ config.name }}</td>
              <td class="px-6 py-3 text-left whitespace-nowrap">{{ formatDate(config.created_at) }}</td>
              <td class="px-6 py-3 text-left whitespace-nowrap">{{ formatDate(config.modified_at) }}</td>
              <td class="px-6 py-3 text-left whitespace-nowrap">{{ config.last_used_with_version || '-' }}</td>
              <td class="px-6 py-3 text-left whitespace-nowrap">
                <button @click="deleteConfig(config.id)" class="px-3 py-1 text-xs text-white transition-colors duration-200 bg-red-500 rounded hover:bg-red-600">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="configs.length === 0" class="p-8 text-center text-gray-600">No configurations found.</div>
      </div>
    </main>

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

    <!-- User Profile Modal -->
    <EditProfileModal 
      v-if="showUserModal" 
      :user="user" 
      @close="showUserModal = false" 
      @success="handlePasswordUpdateSuccess" 
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'
import EditProfileModal from '../components/EditProfileModal.vue'

interface Config {
  id: number
  name: string
  content: string
  last_used_with_version: string | null
  created_at: string
  modified_at: string | null
}

interface User {
  id: number
  username: string
  config_sync_token: string
  created_at: string
  modified_at: string | null
}

const configs = ref<Config[]>([])
const user = ref<User | null>(null)
const showToken = ref(false)
const copied = ref(false)
const showRefreshConfirm = ref(false)
const showUserModal = ref(false)
const loading = ref(true)
const error = ref('')
const router = useRouter()

const copyToken = async () => {
  if (user.value?.config_sync_token) {
    try {
      await navigator.clipboard.writeText(user.value.config_sync_token)
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

const fetchUser = async () => {
  try {
    const response = await api.get('/1/user')
    user.value = response.data
  } catch (err: any) {
    error.value = 'Failed to load user info'
  }
}

const refreshToken = () => {
  showRefreshConfirm.value = true
}

const performRefresh = async () => {
  showRefreshConfirm.value = false
  try {
    const response = await api.get('/1/user/refresh_config_sync_token')
    if (user.value) {
      user.value.config_sync_token = response.data.config_sync_token
    }
  } catch (err: any) {
    alert('Failed to refresh token')
  }
}

const openUserModal = () => {
  showUserModal.value = true
}

const handlePasswordUpdateSuccess = () => {
  alert('Password updated successfully. Please login again.')
  logout()
}

const fetchConfigs = async () => {
  try {
    const response = await api.get('/1/configs')
    configs.value = response.data
  } catch (err: any) {
    error.value = 'Failed to load configurations'
  } finally {
    loading.value = false
  }
}

const init = async () => {
  loading.value = true
  await Promise.all([fetchUser(), fetchConfigs()])
  loading.value = false
}

const deleteConfig = async (id: number) => {
  if (!confirm('Are you sure you want to delete this config?')) return

  try {
    await api.delete(`/1/configs/${id}`)
    await fetchConfigs()
  } catch (err: any) {
    alert('Failed to delete config')
  }
}

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

const formatDate = (dateStr: string | null) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString()
}

onMounted(() => {
  init()
})
</script>
