<template>
  <RouterView v-slot="{ Component }">
    <Transition name="opacity">
      <component :is="Component" />
    </Transition>
  </RouterView>
</template>

<script setup lang="ts">
import { defaults, difficultyLevels, songTypes } from '@/data/defaults'
import { useSongs } from '@/stores/songs'
import { useSessionStorage } from '@vueuse/core'
import { onBeforeMount } from 'vue'

import type { CacheSession } from '@/types'

const sessionCache = useSessionStorage<CacheSession>('cache', defaults.cache, {
  serializer: {
    read(raw) {
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
    write(value) {
      return JSON.stringify(value)
    }
  }
})

const songsStore = useSongs()

songsStore.$subscribe((_, state) => {
  state.cache = sessionCache.value
})

onBeforeMount(() => {
  songsStore.cache = sessionCache.value
})
</script>
