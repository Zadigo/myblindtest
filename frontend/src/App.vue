<template>
  <RouterView />
</template>

<script lang="ts" setup>
import { defaults, difficultyLevels, songTypes } from '@/data/defaults';
import { useSongs } from '@/stores/songs';
import type { CacheSession } from '@/types';
import { useSessionStorage } from '@vueuse/core';
import { onBeforeMount } from 'vue';

const sessionCache = useSessionStorage<CacheSession>('cache', null, {
  serializer: {
    read (raw) {
      const data = JSON.parse(raw) as CacheSession
      
      if (data) {
        if (!difficultyLevels.includes(data.settings.difficultyLevel)) {
          throw new Error('Invalid difficulty level')
        }
        
        if (!songTypes.includes(data.settings.songType)) {
          throw new Error('Invalid song type value')
        }
      }

      return data
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
