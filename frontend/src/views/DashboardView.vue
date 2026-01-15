<template>
  <div class="dashboard-container">
    <header>
      <h1>Config Management</h1>
      <button @click="logout" class="logout-btn">Logout</button>
    </header>
    <main>
      <div v-if="loading" class="loading">Loading...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else class="config-list">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Created At</th>
              <th>Modified At</th>
              <th>Last Used Version</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="config in configs" :key="config.id">
              <td>{{ config.id }}</td>
              <td>{{ config.name }}</td>
              <td>{{ formatDate(config.created_at) }}</td>
              <td>{{ formatDate(config.modified_at) }}</td>
              <td>{{ config.last_used_with_version || '-' }}</td>
              <td>
                <button @click="deleteConfig(config.id)" class="delete-btn">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="configs.length === 0" class="no-data">No configurations found.</div>
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

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.logout-btn {
  padding: 0.5rem 1rem;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.logout-btn:hover {
  background-color: #c82333;
}

.delete-btn {
  padding: 0.25rem 0.5rem;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.delete-btn:hover {
  background-color: #c82333;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background-color: #f8f9fa;
  font-weight: 600;
}

tr:hover {
  background-color: #f8f9fa;
}

.loading, .error, .no-data {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
  color: #666;
}

.error {
  color: #dc3545;
}
</style>
