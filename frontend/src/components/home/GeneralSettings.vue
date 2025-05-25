<template>
  <Card class="border-0 shadow-md">
    <CardContent>
      <CardHeader>
        <CardTitle>
          General settings
        </CardTitle>
      </CardHeader>

      <Input v-model="songStore.cache.settings.rounds" type="number" min="1" max="100" placeholder="Number of rounds" variant="solo-filled" clearable flat />

      <div>
        <Label for="game-difficulty" class="mt-3">
          Game difficulty
        </Label>

        <Select id="game-difficulty" v-model="selectedDifficulty">
          <SelectTrigger class="w-full">
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

        <Label for="song-type" class="mt-3">
          Genre
        </Label>

        <Select id="song-type" v-model="selectedSongType">
          <SelectTrigger class="w-full">
            <SelectValue placeholder="All" />
          </SelectTrigger>

          <SelectContent>
            <SelectGroup v-for="songType in songGenres" :key="songType">
              <SelectItem :value="songType">
                {{ songType }}
              </SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>
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
        <Input id="game-difficulty" v-model="selectedTimeLimit" type="time" placeholder="Time limit" />
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
    </CardContent>
  </Card>
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
