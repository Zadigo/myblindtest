<template>
  <volt-card class="border-0 bg-brand-shade-3/30 shadow-none">
    <template #title>
      <h3 class="font-bold">
        General settings
      </h3>
    </template>

    <template v-if="currentSettings" #content>
      <volt-input-number v-model="currentSettings.settings.rounds" :min="1" :max="100" class="w-full" placeholder="Number of rounds" />

      <div>
        <label>Game difficulty</label>
        <volt-select v-model="currentSettings.settings.difficultyLevel" :options="difficultyLevels.map(x => ({ name: x }))" option-label="name" option-value="name" />

        <label>Genre</label>
        <volt-select v-model="currentSettings.settings.songType" :options="songGenres.map(x => ({ name: x }))" option-label="name" option-value="name" />
      </div>
      
      <div class="mt-3">
        <volt-label for="game-difficulty" class="mb-2">Time limit</volt-label>
        <volt-input-text id="game-difficulty" v-model="currentSettings.settings.timeLimit" type="time" placeholder="Time limit" />
      </div>

      <p for="time-period" class="font-bold mt-10">
        Time period
      </p>

      <p class="font-light">
        Choose a timeframe in years to select the
        period in which the songs should be located
        for the blind test
      </p>

      <!-- <v-range-slider v-model="songStore.settings.timeRange" :min="minimumPeriod" :max="maximumPeriod" :step="1" class="align-center" hide-details>
        <template #prepend>
          <v-text-field v-model="songStore.settings.timeRange[0]" :min="0" density="compact" style="width: 70px" type="number" variant="outlined" hide-details single-line />
        </template>

        <template #append>
          <v-text-field v-model="songStore.settings.timeRange[1]" :min="0" density="compact" style="width: 70px" type="number" variant="outlined" hide-details single-line />
        </template>
      </v-range-slider> -->
    </template>

    <template v-else #content>
      <volt-skeleton class="h-96" />
    </template>
  </volt-card>
</template>

<script setup lang="ts">
import { useSessionStore } from '@/stores/session'

const sessionStore = useSessionStore()
const { currentSettings } = storeToRefs(sessionStore)
</script>
