<template>
  <nuxt-layout>
    <nuxt-page />
  </nuxt-layout>
</template>

<script setup lang="ts">
useDarkMode()

/**
 * Session
 */

const { create } = useCreateSession()
await create()

useHTMLLangAttribute()

/**
 * Theme
 */

const bgTheme = ['dark:bg-primary-950', 'bg-no-repeat', 'bg-center', 'bg-gradient-to-tl', 'from-primary/30', 'via-primary-20', 'to-primary/10']

onMounted(() => {
  document.documentElement.classList.add(...bgTheme)

  const langAttribute = document.createAttribute('lang')
  langAttribute.value = useI18n().locale.value
})

onUnmounted(() => {
  document.documentElement.classList.remove(...bgTheme)
})
</script>
