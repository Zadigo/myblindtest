<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup lang="ts">
import { SplashScreen } from '@capacitor/splash-screen'

await SplashScreen.show({
  showDuration: 2000,
  autoHide: true
})
</script>
