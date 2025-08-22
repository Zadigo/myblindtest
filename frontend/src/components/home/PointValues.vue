<template>
  <VoltCard class="border-0 bg-brand-shade-3/30 shadow-none">
    <template #title>
      <h3 class="font-bold">
        Point value and bonuses
      </h3>
    </template>

    <template #content>
      <volt-input-number v-model="currentSettings.cache.settings.pointValue" :min="1" :step="1" :max="50" />

      <div class="py-3">
        <volt-label>
          <volt-switch v-model="currentSettings.cache.settings.songDifficultyBonus" />
          <label for="">Use song difficulty bonus</label>
        </volt-label>
      </div>

      <div class="py-3">
        <volt-label>
          <volt-switch v-model="currentSettings.cache.settings.speedBonus" />
          <label for="">Use answering speed bonus</label>
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
