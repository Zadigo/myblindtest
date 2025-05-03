import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { defaults } from '../data'

import type { Answer, CacheSession } from '../types'

export const useSongs = defineStore('songs', () => {
  const cache = ref<CacheSession>(defaults.cache)

  const answers = ref<Answer[]>([])
  const correctAnswers = ref<Answer[]>([])

  const scoringTimelineBase = ref<number>(100)
  const scoringTimeline = ref<number[]>([])

  const gameStarted = ref<boolean>(false)

  const firstTeamScore = computed(() => cache.value.teams[0].score)
  const secondTeamScore = computed(() => cache.value.teams[1].score)

  /**
   * Returns the currect song on which the
   * players will be trying to guess
   */
  const currentSong = computed(() => cache.value.songs[cache.value.songs.length - 1])

  return {
    cache,
    answers,
    gameStarted,
    scoringTimelineBase,
    scoringTimeline,
    firstTeamScore,
    secondTeamScore,
    correctAnswers,
    currentSong
  }
})
