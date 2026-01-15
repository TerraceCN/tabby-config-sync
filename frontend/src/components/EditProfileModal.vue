<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
    <div class="w-full max-w-sm p-6 mx-4 bg-white rounded shadow-lg">
      <h3 class="mb-4 text-lg font-bold text-gray-800">Edit Profile</h3>
      <div class="mb-4">
          <label class="block mb-2 text-sm font-bold text-gray-700">Username</label>
          <input type="text" :value="user?.username" readonly class="w-full px-3 py-2 leading-tight text-gray-700 border rounded shadow appearance-none bg-gray-100 focus:outline-none focus:shadow-outline">
      </div>
      <div class="mb-6">
          <label class="block mb-2 text-sm font-bold text-gray-700">New Password</label>
          <input v-model="newPassword" type="password" placeholder="Enter new password" class="w-full px-3 py-2 leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline focus:border-blue-500">
      </div>
      <div class="flex justify-end space-x-4">
        <button @click="$emit('close')" class="px-4 py-2 text-gray-600 transition-colors hover:text-gray-800">Cancel</button>
        <button @click="updateUser" class="px-4 py-2 text-white transition-colors bg-blue-500 rounded hover:bg-blue-600" :disabled="!newPassword">Save</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '../services/api'

interface User {
  username: string
}

defineProps<{
  user: User | null
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'success'): void
}>()

const newPassword = ref('')

const updateUser = async () => {
  if (!newPassword.value) return
  
  try {
    await api.patch('/1/users', { password: newPassword.value })
    emit('success')
  } catch (err: any) {
    alert(err.response?.data?.detail || 'Failed to update password')
  }
}
</script>
