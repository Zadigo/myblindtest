<template>
  <RouterView />
</template>

<script lang="ts" setup>
import { useSongs } from '@/stores/songs';
import { useSessionStorage } from '@vueuse/core';
import type { CacheSession } from '@/types';
import { onBeforeMount } from 'vue';

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
    sessionCache.value = {
        songs: [],
        currentStep: 0,
        teams: [
            {
                name: '',
                score: 0,
                players: []
            },
            {
                name: '',
                score: 0,
                players: []
            }
        ],
        settings: {
            rounds: 1,
            timeLimit: 0
        }
    }
  }
})
</script>
