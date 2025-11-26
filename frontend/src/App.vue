<template>
  <section id="site">
    <volt-toast />

    <router-view v-slot="{ Component }">
      <transition enter-active-class="duration-300 ease-out" enter-from-class="opacity-0 -translate-x-10" enter-to-class="opacity-100 translate-x-0" leave-active-class="duration-300 ease-in" leave-from-class="opacity-100 translate-x-0" leave-to-class="opacity-0 translate-x-10" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </section>
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
