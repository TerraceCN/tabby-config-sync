<template>
  <div class="container px-4 py-8 mx-auto">
    <header class="flex items-center justify-between pb-4 mb-8 border-b border-gray-200">
      <h1 class="text-2xl font-bold text-gray-800">Config Management</h1>
      <button @click="logout" class="px-4 py-2 text-white transition-colors duration-200 bg-red-500 rounded hover:bg-red-600">Logout</button>
    </header>
    <main>
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

interface Config {
  id: number
  name: string
  content: string
  last_used_with_version: string | null
  created_at: string
  modified_at: string | null
}

const configs = ref<Config[]>([])
const loading = ref(true)
const error = ref('')
const router = useRouter()

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
  fetchConfigs()
})
</script>
