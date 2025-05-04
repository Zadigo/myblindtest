<template>
  <section id="site">
    <Toaster />

    <RouterView v-slot="{ Component }">
      <Transition name="opacity">
        <component :is="Component" />
      </Transition>
    </RouterView>
  </section>
</template>

<script setup lang="ts">
import { defaults, difficultyLevels, songGenres } from '@/data'
import { Toaster } from 'vue-sonner'

import type { CacheSession } from '@/types'

const sessionCache = useSessionStorage<CacheSession>('cache', defaults.cache, {
  serializer: {
    read(raw) {
      const data = JSON.parse(raw) as CacheSession

      if (data) {
        if (!difficultyLevels.includes(data.settings.difficultyLevel)) {
          throw new Error('Invalid difficulty level')
        }

        if (!songGenres.includes(data.settings.songType)) {
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
const { cache } = storeToRefs(songsStore)

watch(sessionCache, (newValue) => {
  cache.value = newValue
})

onBeforeMount(() => {
  songsStore.cache = sessionCache.value
})
</script>
