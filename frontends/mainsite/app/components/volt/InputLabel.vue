<template>
  <div class="flex-col justify-start space-y-1">
    <p class="font-semibold">{{ label }}</p>
    <slot />
  </div>
</template>

<script setup lang="ts">
defineProps<{ label: string }>()
</script>
