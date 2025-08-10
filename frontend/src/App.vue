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

const sessionCache = useStorage<CacheSession>('cache', defaults.cache)

const songsStore = useSongs()
const { cache } = storeToRefs(songsStore)

const teamsStore = useTeamsStore()
const { teams } = storeToRefs(teamsStore)

watch(sessionCache, (newValue) => {
  cache.value = newValue
  teams.value = newValue.teams
})

onBeforeMount(() => {
  songsStore.cache = sessionCache.value
  teams.value = sessionCache.value.teams
})
</script>
