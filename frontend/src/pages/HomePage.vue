<template>
  <VContainer>
    <v-row class="my-6 position-relative">
      <v-col cols="6" offset="2">
        <v-card>
          <template #title>
            General settings
          </template>

          <v-card-text>
            <v-text-field v-model="songStore.cache.settings.rounds" type="number" min="1" max="100" placeholder="Number of rounds" variant="solo-filled" clearable flat />

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
          </v-card-text>
        </v-card>

        <v-card class="my-2">
          <template #title>
            Point value and bonuses
          </template>

          <v-card-text>
            <v-form @submit.prevent>
              <v-text-field v-model.number="songStore.cache.settings.pointValue" type="number" min="1" placeholder="Point value" variant="solo-filled" flat />
              <v-switch v-model="songStore.cache.settings.songDifficultyBonus" label="Use song difficulty bonus" inset hide-details />

              <v-divider class="my-2" />

              <v-switch v-model="songStore.cache.settings.speedBonus" label="Use answering speed bonus" inset hide-details />
            </v-form>
          </v-card-text>
        </v-card>

        <v-card>
          <template #title>
            Game modes
          </template>

          <v-card-text>
            <v-switch v-model="songStore.cache.settings.soloMode" label="Run in solo mode" inset hide-details />
            <v-switch v-model="songStore.cache.settings.adminPlays" label="Admin is registered in a team" inset hide-details />
          </v-card-text>
        </v-card>
      </v-col>

      <v-col id="side-panel" tag="aside" cols="3">
        <v-card id="panel">
          <v-card-text>
            <p>
              Guess the artist for each <span class="badge badge-success">{{ songStore.cache.settings.songType }}</span>
              songs that plays. Each correct answers worths <span class="badge badge-warning">{{ songStore.cache.settings.pointValue }} point(s)</span>.
            </p>

            <p v-if="useNumberOfRounds">
              Players have {{ songStore.cache.settings.rounds }} rounds until a winner is determined
            </p>

            <p v-html="difficultyLevelPhrase" />

            <p v-if="songStore.cache.settings.songDifficultyBonus">
              Each point will vary based on the song's difficulty. For example, if a song has a
              <b>2 stars</b> difficuly, the points for a correct answer will be multiplied by 4. So, if
              a correct answer is normally worth 1 point, it would instead be worth <b>2 points</b>.
            </p>

            <p v-if="useTimeLimit">
              There is a time limit of <span class="badge badge-warning">5 minutes</span>. The team with the highest
              score at the end of the time wins
            </p>
          </v-card-text>

          <v-card-actions>
            <v-btn to="/teams" color="primary" variant="tonal" rounded>
              Manage teams
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </VContainer>
</template>

<script lang="ts" setup>
import { songTypes, difficultyLevels } from '@/data/defaults'
import { useAxiosClient } from '@/plugins/client'
import { useSongs } from '@/stores/songs'
import { GenreDistribution, SettingsDataApiResponse } from '@/types'
import { useHead } from 'unhead'
import { computed, onBeforeMount, ref } from 'vue'
import { toast } from 'vue-sonner'

useHead({
  title: 'Réglages'
})

const { client } = useAxiosClient()
const songStore = useSongs()

// TODO: Place in cache
const minimumPeriod = ref<number>(0)
const maximumPeriod = ref<number>(100)
const genreDistribution = ref<GenreDistribution[]>([])

const difficultyLevelPhrase = computed(() => {
  if (songStore.cache.settings.difficultyLevel === 'All') {
    return `All songs will have varying difficulty levels`
  } else {
    return `All songs will be set to an 
    <span class="badge badge-success">${songStore.cache.settings.difficultyLevel}</span> 
    difficulty level`
  }
})

const useTimeLimit = computed(() => {
  return songStore.cache.settings.timeLimit !== null
})

const useNumberOfRounds = computed(() => {
  return songStore.cache.settings.rounds !== null
})

async function requestSettingsData() {
  try {
    const response = await client.get<SettingsDataApiResponse>('/songs/settings')

    songStore.cache.settings.timeRange[0] = response.data.period.minimum
    songStore.cache.settings.timeRange[1] = response.data.period.maximum

    minimumPeriod.value = response.data.period.minimum
    maximumPeriod.value = response.data.period.maximum

    genreDistribution.value = response.data.count_by_genre
  } catch (e) {
    toast.error('Could not get settings')
  }
}

onBeforeMount(requestSettingsData)
</script>

<style lang="scss">
#side-panel {
  #panel {
    position: sticky;
    top: 0;
    left: 0;
  }
}
</style>
