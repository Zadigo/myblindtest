<template>
  <div class="grid grid-cols-3 md:grid-cols-4 items-center gap-2 w-full">
    <p class="col-span-2 md:col-span-3">
      <slot />
    </p>
    
    <volt-toggle-switch v-model="switchValue" class="place-self-center" :disabled="true" />
  </div>
</template>

<script setup lang="ts">
const switchValue = defineModel('switchValue', { type: Boolean, default: false })
</script>
s
