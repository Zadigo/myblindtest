<template>
  <VoltCard class="border-0 bg-brand-shade-3/30 shadow-none">
    <template #title>
      <h3 class="font-bold">
        Game modes
      </h3>
    </template>

    <template #content>
      <div class="py-3">
        <volt-label>
          <volt-switch v-model="currentSettings.cache.settings.soloMode" />
          <label>Run in solo mode</label>
        </volt-label>
      </div>

      <div class="py-3">
        <volt-label>
          <volt-switch v-model="currentSettings.cache.settings.adminPlays" />
          <label>Admin is registered in a team</label>
        </volt-label>
      </div>
    </template>
  </VoltCard>
</template>

<script setup lang="ts">
import { useSessionStore } from '@/stores/session'

const sessionStore = useSessionStore()
const { currentSettings } = storeToRefs(sessionStore)
</script>
