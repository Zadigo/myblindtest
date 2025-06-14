<template>
  <VoltCard class="border-0 bg-brand-shade-3/30 shadow-none">
    <template #title>
      <h3 class="font-bold">
        Game modes
      </h3>
    </template>

    <template #content>
      <div class="py-3">
        <VoltLabel>
          <VoltSwitch v-model="songStore.cache.settings.soloMode" />
          <label>Run in solo mode</label>
        </VoltLabel>
      </div>

      <div class="py-3">
        <VoltLabel>
          <VoltSwitch v-model="songStore.cache.settings.adminPlays" />
          <label>Admin is registered in a team</label>
        </VoltLabel>
      </div>
    </template>
  </VoltCard>
</template>

<script setup lang="ts">
import { useSongs } from '@/stores/songs'

const songStore = useSongs()
</script>
