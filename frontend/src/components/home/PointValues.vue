<template>
  <volt-card class="border-0 bg-brand-shade-3/30">
    <template #title>
      <h3 class="font-bold">
        Point value and bonuses
      </h3>
    </template>

    <template v-if="currentSettings" #content>
      <!-- Points -->
      <volt-input-number v-model="currentSettings.settings.pointValue" :min="1" :step="1" :max="20" class="w-full" />

      <!-- Song Difficulty Bonus -->
      <div class="py-3">
        <volt-label label-for="song-difficulty" label="Use song difficulty bonus">
          <volt-toggle-switch v-model="currentSettings.settings.songDifficultyBonus" />
        </volt-label>
      </div>

      <!-- Speed Bonus -->
      <div class="py-3">
        <volt-label label-for="speed-bonus" label="Use answering speed bonus">
          <volt-toggle-switch v-model="currentSettings.settings.speedBonus" :disabled="true" />
        </volt-label>
      </div>

      <div class="py-3">
        <volt-fieldset legend="Epic game mode">
          <div class="grid grid-cols-3 md:grid-cols-4 items-center gap-2 w-full">
            <p class="col-span-3">Every wrong answer costs points (which can depend on the difficulty of the song)</p>
            <volt-toggle-switch class="place-self-center" :disabled="true" />
          </div>
        </volt-fieldset>
      </div>
    </template>

    <template v-else #content>
      <div class="space-y-2">
        <volt-skeleton height="100px" />
        <volt-skeleton height="100px" />
        <volt-skeleton height="100px" />
      </div>
    </template>
  </volt-card>
</template>

<script setup lang="ts">
const { currentSettings } = useSession()
</script>
