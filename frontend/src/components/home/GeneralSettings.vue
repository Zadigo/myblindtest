<template>
  <Card class="border-0 shadow-md">
    <CardHeader>
      <CardTitle>
        General settings
      </CardTitle>
    </CardHeader>

    <CardContent>
      <Input v-model="songStore.cache.settings.rounds" type="number" min="1" max="100" placeholder="Number of rounds" variant="solo-filled" clearable flat />

      <div>
        <Label for="game-difficulty">
          Game difficulty
        </Label>

        <Select id="game-difficulty" v-model="selectedDifficulty">
          <SelectTrigger>
            <SelectValue placeholder="All" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup v-for="difficultyLevel in difficultyLevels" :key="difficultyLevel">
              <SelectItem :value="difficultyLevel">
                {{ difficultyLevel }}
              </SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>

        <Label for="song-type">
          Genre
        </Label>

        <Select id="song-type" v-model="selectedSongType">
          <SelectTrigger>
            <SelectValue placeholder="All" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup v-for="songType in songTypes" :key="songType">
              <SelectItem :value="songType">
                {{ songType }}
              </SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>
      </div>

      <!-- <v-select id="song-type" v-model="songStore.cache.settings.songType" :items="songTypes" variant="solo-filled" flat /> -->
      <!-- <v-autocomplete :items="genreDistribution" item-value="genre" auto-select-first solo>
        <template #item="{ props, item }">
          <v-list-item v-bind="props" :title="item.raw.genre">
            <v-chip>{{ item.raw.count }}</v-chip>
          </v-list-item>
        </template>
      </v-autocomplete> -->

      <Label for="game-difficulty">
        Time limit
      </Label>
      <Input id="game-difficulty" v-model="selectedTimeLimit" type="time" placeholder="Time limit" />

      <label for="time-period" class="fw-bold">
        Time period
      </label>

      <p class="font-light">
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
import type { DifficultyLevels, SongGenres } from '@/types'
// import { GenreDistribution } from '@/types'
import { ref } from 'vue'

const songStore = useSongs()
const selectedTimeLimit = ref<string | number>(0)
const selectedDifficulty = ref<DifficultyLevels>('All')
const selectedSongType = ref<SongGenres>('All')
const minimumPeriod = ref<number>(0)
const maximumPeriod = ref<number>(100)

// const selectedTimeRane = ref<number[]>([0, 0])
// const genreDistribution = ref<GenreDistribution[]>([])
</script>
