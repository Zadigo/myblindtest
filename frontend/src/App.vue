<template>
  <RouterView />
</template>

<script lang="ts" setup>
import { useSongs } from '@/stores/songs';
import type { CacheSession } from '@/types';
import { useSessionStorage } from '@vueuse/core';
import { onBeforeMount } from 'vue';
import defaults from '@/data/defaults.json'

const sessionCache = useSessionStorage<CacheSession>('cache', null, {
  serializer: {
    read (raw) {
      return JSON.parse(raw)
    },
    write (value) {
      return JSON.stringify(value)
    }
  }
})

const songsStore = useSongs()

songsStore.$subscribe(({ storeId }) => {
  if (storeId === 'songs') {
    sessionCache.value = songsStore.cache
  }
})

onBeforeMount(() => {
  if (!sessionCache.value) {
    sessionCache.value = defaults.cache
  }
})
</script>
