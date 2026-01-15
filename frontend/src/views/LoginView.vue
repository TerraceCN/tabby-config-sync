<template>
  <div class="flex min-h-screen items-center justify-center bg-gray-100">
    <div class="w-full max-w-sm bg-white p-8 rounded-lg shadow-md">
      <h2 class="mb-6 text-center text-2xl font-bold text-gray-800">Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block mb-2 text-sm font-bold text-gray-700" for="username">Username</label>
          <input
            class="w-full px-3 py-2 leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline"
            type="text"
            id="username"
            v-model="username"
            required
          />
        </div>
        <div class="mb-6">
          <label class="block mb-2 text-sm font-bold text-gray-700" for="password">Password</label>
          <input
            class="w-full px-3 py-2 mb-3 leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline"
            type="password"
            id="password"
            v-model="password"
            required
          />
        </div>
        <button
          class="w-full px-4 py-2 font-bold text-white bg-blue-500 rounded hover:bg-blue-700 focus:outline-none focus:shadow-outline"
          type="submit"
        >
          Login
        </button>
        <p v-if="error" class="mt-4 text-center text-red-500 text-xs italic">{{ error }}</p>
        <div class="mt-4 text-center">
          <router-link to="/register" class="text-blue-500 hover:text-blue-700 text-sm">
            Don't have an account? Register
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const handleLogin = async () => {
  try {
    const formData = new URLSearchParams()
    formData.append('username', username.value)
    formData.append('password', password.value)

    const response = await api.post('/token', formData)
    const token = response.data.access_token
    localStorage.setItem('token', token)
    router.push('/')
  } catch (err: any) {
    error.value = 'Invalid username or password'
  }
}
</script>
