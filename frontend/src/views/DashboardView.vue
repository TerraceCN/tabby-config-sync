<template>
  <div class="container px-4 py-8 mx-auto">
    <header class="flex items-center justify-between pb-4 mb-8 border-b border-gray-200">
      <div class="flex items-center space-x-3">
        <img src="/logo.svg" alt="Tabby Config Sync" class="h-8" />
        <h1 class="text-2xl font-bold text-gray-800">Dashboard</h1>
      </div>
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
        @view="viewConfig"
      />
    </main>

    <!-- User Profile Modal -->
    <EditProfileModal
      v-if="showUserModal"
      :user="user"
      @close="showUserModal = false"
      @success="handlePasswordUpdateSuccess"
    />

    <!-- Config Detail Modal -->
    <ConfigDetailModal
      v-if="showConfigDetail"
      :show="showConfigDetail"
      :config="selectedConfig"
      @close="showConfigDetail = false"
    />

    <!-- Footer -->
    <footer class="mt-12 pt-6 border-t border-gray-200 text-center text-sm text-gray-500">
      <a
        href="https://github.com/TerraceCN/tabby-config-sync"
        target="_blank"
        rel="noopener noreferrer"
        class="inline-flex items-center gap-2 hover:text-gray-700 transition-colors"
      >
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd" />
        </svg>
        <span>TerraceCN/tabby-config-sync</span>
      </a>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'
import EditProfileModal from '../components/EditProfileModal.vue'
import TokenDisplay from '../components/TokenDisplay.vue'
import ConfigList, { type Config } from '../components/ConfigList.vue'
import ConfigDetailModal from '../components/ConfigDetailModal.vue'

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
const showConfigDetail = ref(false)
const selectedConfig = ref<Config | null>(null)
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

const viewConfig = (config: Config) => {
  selectedConfig.value = config
  showConfigDetail.value = true
}

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

onMounted(() => {
  init()
})
</script>
