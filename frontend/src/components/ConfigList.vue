<template>
  <div v-if="loading" class="p-8 text-center text-gray-600">
    <div class="flex flex-col items-center justify-center">
      <svg class="w-8 h-8 mb-4 text-blue-500 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <span>Loading configurations...</span>
    </div>
  </div>
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
            <button @click="$emit('view', config)" class="px-3 py-1 mr-2 text-xs text-white transition-colors duration-200 bg-blue-500 rounded hover:bg-blue-600">View</button>
            <button @click="$emit('delete', config.id)" class="px-3 py-1 text-xs text-white transition-colors duration-200 bg-red-500 rounded hover:bg-red-600">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="configs.length === 0" class="p-8 text-center text-gray-600">No configurations found.</div>
  </div>
</template>

<script setup lang="ts">
export interface Config {
  id: number
  name: string
  content: string
  last_used_with_version: string | null
  created_at: string
  modified_at: string | null
}

defineProps<{
  configs: Config[]
  loading: boolean
}>()

defineEmits<{
  (e: 'delete', id: number): void
  (e: 'view', config: Config): void
}>()

const formatDate = (dateStr: string | null) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString()
}
</script>
