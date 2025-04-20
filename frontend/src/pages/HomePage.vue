<template>
  <section class="mx-auto px-10 relative">
    <div class="grid grid-cols-2 my-6 gap-4">
      <div>
        <GeneralSettings />
        <PointValues />
        <GameModes />
      </div>

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
    </div>
  </section>
</template>

<script lang="ts" setup>
import { useAxiosClient } from '@/plugins/client'
import { useSongs } from '@/stores/songs'
import { GenreDistribution, SettingsDataApiResponse } from '@/types'
import { computed, onBeforeMount, ref } from 'vue'
import { toast } from 'vue-sonner'

import GeneralSettings from '@/components/home/GeneralSettings.vue'
import PointValues from '@/components/home/PointValues.vue'
import GameModes from '@/components/home/GameModes.vue'

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

/**
 *
 */
async function requestSettingsData() {
  try {
    const response = await client.get<SettingsDataApiResponse>('/songs/settings')

    songStore.cache.settings.timeRange[0] = response.data.period.minimum
    songStore.cache.settings.timeRange[1] = response.data.period.maximum

    minimumPeriod.value = response.data.period.minimum
    maximumPeriod.value = response.data.period.maximum

    genreDistribution.value = response.data.count_by_genre
  } catch {
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
