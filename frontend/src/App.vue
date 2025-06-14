<template>
  <section id="site">
    <Toaster />

    <RouterView v-slot="{ Component }">
      <Transition enter-active-class="duration-300 ease-out" enter-from-class="opacity-0 -translate-x-10" enter-to-class="opacity-100 translate-x-0" leave-active-class="duration-300 ease-in" leave-from-class="opacity-100 translate-x-0" leave-to-class="opacity-0 translate-x-10" mode="out-in">
        <component :is="Component" />
      </Transition>
    </RouterView>
  </section>
</template>

<script setup lang="ts">
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
