<template>
  <section class="w-5xl mx-auto px-10 my-20 relative">
    <volt-card class="mt-10 mb-5 shadow-none">
      <template #content>
        <div class="flex justify-end">
          <volt-button class="rounded-full">
            <router-link :to="{ name: 'teams' }" class="inline-flex gap-2 items-center">
              Manage teams
              <vue-icon icon="i-fa7-solid:arrow-right" />
            </router-link>
          </volt-button>
        </div>
      </template>
    </volt-card>

    <div class="grid grid-cols-2 gap-2">
      <general-settings />
      <point-values />
      <game-modes />
    </div>
  </section>
</template>

<script setup lang="ts">
import { useSessionStore } from '@/stores/session'

useLoadAutocompleteData()

const { sessionId, create } = useSessionStore()
onBeforeMount(async () => {
  await create()
})
</script>

<style lang="scss">
#side-panel {
  #panel {
    position: sticky;
    top: 0;
    left: 0;
  }
}
</style>
