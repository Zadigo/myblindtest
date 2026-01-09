<template>
  <volt-card class="border-0 bg-brand-shade-3/30">
    <template #title>
      <h3 class="font-bold">
        {{ $t('General settings') }}
      </h3>
    </template>
    
    <template v-if="currentSettings" #content>
      <volt-input-label :label="$t('Number of rounds')">
        <volt-input-number v-model="currentSettings.settings.rounds" :min="0" :max="100" class="w-full" />
      </volt-input-label>

      <div classs="space-y-3">
        <volt-input-label :label="$t('Game difficulty')">
          <volt-select v-model="currentSettings.settings.difficultyLevel" :options="difficultyLevels.map(x => ({ name: x }))" class="w-4/6" option-label="name" option-value="name" />
        </volt-input-label>

        <volt-input-label :label="$t('Genre')">
          <volt-select v-model="currentSettings.settings.genreSelected" :options="genres" class="w-4/6" option-label="name" option-value="name" />
        </volt-input-label>
      </div>

      <div class="mt-3">
        <volt-input-label :label="$t('Time limit')">
          <volt-input-number id="game-difficulty" v-model.number="currentSettings.settings.timeLimit" :min="0" :step="1" />
        </volt-input-label>
      </div>

      <div class="my-5">
        <volt-label label-for="multiple-choice-answers" :label="$t('Multiple choice answers')">
          <volt-toggle-switch id="multiple-choice-answers" v-model="currentSettings.settings.multipleChoiceAnswers" />
        </volt-label>
      </div>

      <p class="font-semibold mt-10">
        {{ $t('Time period') }}
      </p>

      <p class="font-light">
        {{ $t('time_period_text') }}
      </p>
      <volt-slider v-model="currentSettings.settings.timeRange" :min="autocomplete?.period.minimum || 0" :max="autocomplete?.period.maximum || 0" :step="1" class="my-10" range />
    </template>

    <template v-else #content>
      {{ currentSettings }}
      <div class="space-y-2">
        <volt-skeleton height="100px" />
        <volt-skeleton height="100px" />
        <volt-skeleton height="100px" />
      </div>
    </template>
  </volt-card>
</template>

<script setup lang="ts">
import { difficultyLevels } from '~/data'

const { genres, autocomplete } = useLoadAutocompleteData(true)
const { currentSettings } = useSession()
console.log(currentSettings.value)
</script>
