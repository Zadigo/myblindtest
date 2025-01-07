<template>
  <section class="site">
    <Transition class="animate__animated" enter-to-class="animate__slideInDown" enter-from-class="animate__slideInUp">
      <BaseNavbar v-if="$route.name !== 'blind_test'" />
    </Transition>
    
    <Toaster position="top-right" />

    <!-- Main -->
    <RouterView />
  </section>
</template>

<script setup lang="ts">
import { Toaster } from 'vue-sonner';

import BaseNavbar from '@/components/BaseNavbar.vue';
</script>
