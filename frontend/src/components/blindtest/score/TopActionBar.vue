<template>
  <nav class="absolute top-0 left-0 w-full h-auto bg-transparent z-50">
    <div class="w-full p-2 flex justify-end">
      <volt-secondary-button size="small" @click="$emit('toggle-graph')">
        <vue-icon icon="lucide:chart-area" />
      </volt-secondary-button>
    </div>
  </nav>
</template>

<script setup lang="ts">
defineEmits<{ 'toggle-graph': [] }>()
</script>
