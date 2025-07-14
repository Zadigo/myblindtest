<template>
  <VoltCard class="border-0 bg-brand-shade-3/30 shadow-none">
    <template #title>
      <h3 class="font-bold">
        Point value and bonuses
      </h3>
    </template>

    <template #content>
      <VoltInputNumber v-model="songStore.cache.settings.pointValue" :min="1" :step="1" :max="50" />

      <div class="py-3">
        <VoltLabel>
          <VoltSwitch v-model="songStore.cache.settings.songDifficultyBonus" />
          <label for="">Use song difficulty bonus</label>
        </VoltLabel>
      </div>

      <div class="py-3">
        <VoltLabel>
          <VoltSwitch v-model="songStore.cache.settings.speedBonus" />
          <label for="">Use answering speed bonus</label>
        </VoltLabel>
      </div>
    </template>
  </VoltCard>
</template>

<script setup lang="ts">
const songStore = useSongs()
</script>
