<template>
  <div class="py-2">
    <div id="spinner" :class="name" />
  </div>
</template>

<script setup lang="ts">
defineProps({
  name: {
    type: String,
    default: 'loader-1'
  }
})
</script>

<style lang="scss" scoped>
@import url('./spinners.scss');
</style>
