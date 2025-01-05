<template>
  <section class="site">
    <BaseNavbar v-if="$route.name !== 'blind_test'" />
    <Toaster position="top-right" />

    <!-- Main -->
    <RouterView v-slot="{ Component }">
      <Transition name="opacity">
        <component :is="Component" />
      </Transition>
    </RouterView>
  </section>
</template>

<script setup lang="ts">
import { Toaster } from 'vue-sonner';

import BaseNavbar from '@/components/BaseNavbar.vue';
</script>
