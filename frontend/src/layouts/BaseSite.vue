<template>
  <section class="site">
    <Transition name="animate__animated" enter-active-class="animate__animated animate__slideInDown" leave-active-class="animate__animated animate__slideInUp">
      <BaseNavbar v-if="!isStarted" />
    </Transition>

    <Toaster position="top-right" />

    <!-- Main -->
    <RouterView />
  </section>
</template>

<script setup lang="ts">
import { Toaster } from 'vue-sonner'

import BaseNavbar from '@/components/BaseNavbar.vue'
import { useSongs } from '@/stores/songs'

const { isStarted } = useSongs()
</script>
