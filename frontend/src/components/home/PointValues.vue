<template>
  <volt-card class="border-0 bg-brand-shade-3/30">
    <template #title>
      <h3 class="font-bold">
        Point value and bonuses
      </h3>
    </template>

    <template v-if="currentSettings" #content>
      <volt-input-number v-model="currentSettings.settings.pointValue" :min="1" :step="1" :max="50" />

      <div class="py-3">
        <volt-label label-for="song-difficulty" label="Use song difficulty bonus">
          <volt-toggle-switch v-model="currentSettings.settings.songDifficultyBonus" />
        </volt-label>
      </div>

      <div class="py-3">
        <volt-label label-for="speed-bonus" label="Use answering speed bonus">
          <volt-toggle-switch v-model="currentSettings.settings.speedBonus" />
        </volt-label>
      </div>
    </template>

    <template v-else #content>
      <volt-skeleton class="h-96" />
    </template>
  </volt-card>
</template>

<script setup lang="ts">
const { currentSettings } = useSession()
</script>
