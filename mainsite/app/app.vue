<template>
  <nuxt-layout>
    <nuxt-page />
  </nuxt-layout>
</template>

<script setup lang="ts">
useDarkMode()

/**
 * Theme
 */

const bgTheme = ['dark:bg-primary-950', 'bg-no-repeat', 'bg-center', 'bg-gradient-to-tl', 'from-primary/30', 'via-primary-20', 'to-primary/10']

onMounted(() => {
  document.documentElement.classList.add(...bgTheme)
})

onUnmounted(() => {
  document.documentElement.classList.remove(...bgTheme)
})
</script>
