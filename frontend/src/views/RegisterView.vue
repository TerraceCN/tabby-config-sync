<template>
  <div class="flex min-h-screen items-center justify-center bg-gray-100">
    <div class="w-full max-w-sm bg-white p-8 rounded-lg shadow-md">
      <h2 class="mb-6 text-center text-2xl font-bold text-gray-800">Register</h2>
      <form @submit.prevent="handleRegister">
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
        <div class="mb-4">
          <label class="block mb-2 text-sm font-bold text-gray-700" for="password">Password</label>
          <input
            class="w-full px-3 py-2 leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline"
            type="password"
            id="password"
            v-model="password"
            required
          />
        </div>
        <div class="mb-6">
          <label class="block mb-2 text-sm font-bold text-gray-700" for="confirmPassword">Confirm Password</label>
          <input
            class="w-full px-3 py-2 mb-3 leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline"
            type="password"
            id="confirmPassword"
            v-model="confirmPassword"
            required
          />
        </div>
        <button
          class="w-full px-4 py-2 font-bold text-white bg-green-500 rounded hover:bg-green-700 focus:outline-none focus:shadow-outline"
          type="submit"
        >
          Register
        </button>
        <p v-if="error" class="mt-4 text-center text-red-500 text-xs italic">{{ error }}</p>
        <div class="mt-4 text-center">
          <router-link to="/login" class="text-blue-500 hover:text-blue-700 text-sm">
            Already have an account? Login
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
const confirmPassword = ref('')
const error = ref('')
const router = useRouter()

const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  try {
    await api.post('/1/users', {
      username: username.value,
      password: password.value
    })
    // Redirect to login page after successful registration
    router.push('/login')
  } catch (err: any) {
    if (err.response && err.response.data && err.response.data.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = 'Registration failed. Please try again.'
    }
  }
}
</script>
