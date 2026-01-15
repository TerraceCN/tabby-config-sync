<template>
  <div class="container px-4 py-8 mx-auto">
    <header class="flex items-center justify-between pb-4 mb-8 border-b border-gray-200">
      <h1 class="text-2xl font-bold text-gray-800">Dashboard</h1>
      <div class="flex items-center space-x-4">
        <button @click="openUserModal" class="text-gray-600 hover:text-gray-800 focus:outline-none">
          <span v-if="user" class="font-medium">{{ user.username }}</span>
          <span v-else-if="userLoading" class="inline-block w-20 h-5 bg-gray-200 rounded animate-pulse"></span>
          <span v-else>Profile</span>
        </button>
        <button @click="logout" class="px-4 py-2 text-white transition-colors duration-200 bg-red-500 rounded hover:bg-red-600">Logout</button>
      </div>
    </header>
    <main>
      <!-- Token Management Section -->
      <TokenDisplay 
        :token="user?.config_sync_token" 
        :loading="userLoading"
        @update:token="updateToken"
      />

      <div v-if="configsError" class="p-8 text-center text-red-500">{{ configsError }}</div>
      
      <!-- Config List Section -->
      <ConfigList 
        :configs="configs" 
        :loading="configsLoading" 
        @delete="deleteConfig" 
      />
    </main>

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
import TokenDisplay from '../components/TokenDisplay.vue'
import ConfigList, { type Config } from '../components/ConfigList.vue'

interface User {
  id: number
  username: string
  config_sync_token: string
  created_at: string
  modified_at: string | null
}

const configs = ref<Config[]>([])
const user = ref<User | null>(null)
const showUserModal = ref(false)
const userLoading = ref(true)
const configsLoading = ref(true)
const configsError = ref('')
const router = useRouter()

const fetchUser = async () => {
  userLoading.value = true
  try {
    const response = await api.get('/1/user')
    user.value = response.data
  } catch (err: any) {
    console.error('Failed to load user info', err)
  } finally {
    userLoading.value = false
  }
}

const updateToken = (newToken: string) => {
  if (user.value) {
    user.value.config_sync_token = newToken
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
  configsLoading.value = true
  configsError.value = ''
  try {
    const response = await api.get('/1/configs')
    configs.value = response.data
  } catch (err: any) {
    configsError.value = 'Failed to load configurations'
  } finally {
    configsLoading.value = false
  }
}

const init = () => {
  fetchUser()
  fetchConfigs()
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

onMounted(() => {
  init()
})
</script>
