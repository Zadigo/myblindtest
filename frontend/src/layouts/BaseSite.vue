<template>
  <section class="site">
    <BaseNavbar />
    <Toaster position="top-right" />

    <RouterView />
  </section>
</template>

<script setup lang="ts">
import { Toaster } from 'vue-sonner';

import BaseNavbar from '@/components/BaseNavbar.vue';
</script>
