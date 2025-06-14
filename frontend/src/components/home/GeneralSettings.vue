<template>
  <VoltCard class="border-0 bg-brand-shade-3/30 shadow-none">
    <template #title>
      <h3 class="font-bold">
        General settings
      </h3>
    </template>

    <template #content>
      <VoltInputNumber v-model="songStore.cache.settings.rounds" :min="1" :max="100" class="w-full" placeholder="Number of rounds" />

      <div>
        <label>Game difficulty</label>
        <VoltSelect v-model="selectedDifficulty" :options="difficultyLevels.map(x => ({ name: x }))" option-label="name" option-value="name" />

        <label>Genre</label>
        <VoltSelect v-model="selectedSongType" :options="songGenres.map(x => ({ name: x }))" option-label="name" option-value="name" />
      </div>

      <!-- <Combobox>
        <ComboboxTrigger>
          <Input />
        </ComboboxTrigger>

        <ComboboxContent>
          <ComboboxItem v-for="genre in genreDistribution" :key="genre" :value="genre">
            {{ genre }}
          </ComboboxItem>
        </ComboboxContent>
      </Combobox> -->

      <!-- <Select v-model="songStore.cache.settings.songType">
        <SelectTrigger class="w-full">
          <SelectValue />
        </SelectTrigger>

        <SelectContent>
          <SelectItem v-for="songType in songGenres" :key="songType" :value="songType">
            {{ songType }}
          </SelectItem>
        </SelectContent>
      </Select> -->

      <!-- <v-select id="song-type" v-model="songStore.cache.settings.songType" :items="songTypes" variant="solo-filled" flat /> -->
      <!-- <v-autocomplete :items="genreDistribution" item-value="genre" auto-select-first solo>
        <template #item="{ props, item }">
          <v-list-item v-bind="props" :title="item.raw.genre">
            <v-chip>{{ item.raw.count }}</v-chip>
          </v-list-item>
        </template>
      </v-autocomplete> -->

      <div class="mt-3">
        <Label for="game-difficulty" class="mb-2">
          Time limit
        </Label>
        <VoltInputText id="game-difficulty" v-model="selectedTimeLimit" type="time" placeholder="Time limit" />
      </div>

      <p for="time-period" class="font-bold mt-10">
        Time period
      </p>

      <p class="font-light">
        Choose a timeframe in years to select the
        period in which the songs should be located
        for the blind test
      </p>

      <!-- <v-range-slider v-model="songStore.cache.settings.timeRange" :min="minimumPeriod" :max="maximumPeriod" :step="1" class="align-center" hide-details>
        <template #prepend>
          <v-text-field v-model="songStore.cache.settings.timeRange[0]" :min="0" density="compact" style="width: 70px" type="number" variant="outlined" hide-details single-line />
        </template>

        <template #append>
          <v-text-field v-model="songStore.cache.settings.timeRange[1]" :min="0" density="compact" style="width: 70px" type="number" variant="outlined" hide-details single-line />
        </template>
      </v-range-slider> -->
    </template>
  </VoltCard>
</template>

<script setup lang="ts">
const songStore = useSongs()

const selectedTimeLimit = ref<string | number>(0)
const selectedDifficulty = ref<DifficultyLevels>('All')
const selectedSongType = ref<SongGenres>('All')

// const minimumPeriod = ref<number>(0)
// const maximumPeriod = ref<number>(100)

// const selectedTimeRane = ref<number[]>([0, 0])
// const genreDistribution = ref<GenreDistribution[]>([])
</script>
