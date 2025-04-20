<template>
  <Card class="border-0 shadow-md">
    <CardHeader>
      <CardTitle>
        General settings
      </CardTitle>
    </CardHeader>

    <CardContent>
      <Input v-model="songStore.cache.settings.rounds" type="number" min="1" max="100" placeholder="Number of rounds" variant="solo-filled" clearable flat />

      <label for="game-difficulty" class="fw-bold">
        Game difficulty
      </label>
      <v-select id="game-difficulty" v-model="songStore.cache.settings.difficultyLevel" :items="difficultyLevels" variant="solo-filled" flat />

      <label for="song-type" class="fw-bold">
        Genre
      </label>

      <v-select id="song-type" v-model="songStore.cache.settings.songType" :items="songTypes" variant="solo-filled" flat />
      <!-- <v-autocomplete :items="genreDistribution" item-value="genre" auto-select-first solo>
        <template #item="{ props, item }">
          <v-list-item v-bind="props" :title="item.raw.genre">
            <v-chip>{{ item.raw.count }}</v-chip>
          </v-list-item>
        </template>
      </v-autocomplete> -->

      <label for="game-difficulty" class="fw-bold">
        Time limit
      </label>
      <v-text-field v-model="songStore.cache.settings.timeLimit" type="time" variant="solo-filled" clearable flat />

      <label for="game-difficulty" class="fw-bold">
        Time period
      </label>

      <p>
        Choose a timeframe in years to select the
        period in which the songs should be located
        for the blind test
      </p>

      <v-range-slider v-model="songStore.cache.settings.timeRange" :min="minimumPeriod" :max="maximumPeriod" :step="1" class="align-center" hide-details>
        <template #prepend>
          <v-text-field v-model="songStore.cache.settings.timeRange[0]" :min="0" density="compact" style="width: 70px" type="number" variant="outlined" hide-details single-line />
        </template>

        <template #append>
          <v-text-field v-model="songStore.cache.settings.timeRange[1]" :min="0" density="compact" style="width: 70px" type="number" variant="outlined" hide-details single-line />
        </template>
      </v-range-slider>
    </CardContent>
  </Card>
</template>

<script lang="ts" setup>
import { songTypes, difficultyLevels } from '@/data/defaults'
import { useSongs } from '@/stores/songs'
// import { GenreDistribution } from '@/types'
import { ref } from 'vue'

const songStore = useSongs()

const minimumPeriod = ref<number>(0)
const maximumPeriod = ref<number>(100)
// const genreDistribution = ref<GenreDistribution[]>([])
</script>
