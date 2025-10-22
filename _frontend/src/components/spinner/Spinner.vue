<template>
  <div class="py-2">
    <div id="spinner" :class="name" />
  </div>
</template>

<script setup lang="ts">
const { name = 'loader-1' } = defineProps<{ name: string }>()
</script>

<style lang="scss" scoped>
@import url('./spinners.scss');
</style>
