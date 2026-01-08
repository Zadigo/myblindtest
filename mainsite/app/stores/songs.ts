import { defineStore } from 'pinia'

import type { Answer, Song } from '~/types'

/**
 * A store that manages the songs (songs played, current song...)
 */
export const useSongs = defineStore('songs', () => {
  const answers = ref<Answer[]>([])
  const correctAnswers = ref<Answer[]>([])

  const scoringTimelineBase = ref<number>(100)
  const scoringTimeline = ref<number[]>([])
  
  const { inc: incrementStep, reset: resetStep, count: currentStep } = useCounter(0, { min: 0 })
  
  const songsPlayed = ref<Song[]>([])

  // Django returns a list of the remaining songs to be played
  // minus the song that was already played. So, we just have
  // to get the last song of the list to get the current song
  const currentSong = computed(() => songsPlayed.value[songsPlayed.value.length - 1])

  function reset() {
    answers.value = []
    correctAnswers.value = []
    scoringTimelineBase.value = 100
    scoringTimeline.value = []
    songsPlayed.value = []
  }
  
  return {
    /**
     * Reset the store to its initial state
     */
    reset,
    /**
     * The current step in the game. This is used
     * specifically when the user has limited the game
     * to a certain number of rounds
     */
    currentStep,
    /**
     * All the answers of the game
     */
    answers,
    /**
     * The base score for the scoring timeline
     */
    scoringTimelineBase,
    /**
     * The current scoring timeline
     */
    scoringTimeline,
    /**
     * All the correct answers
     */
    correctAnswers,
    /**
     * Songs that were randomly selected
     * to be played in the game
     */
    songsPlayed,
    /**
     * The currently playing song which corresponds
     * to the last song in the list of songs played
     */
    currentSong,
    /**
     * Increments the current step
     */
    incrementStep,
    /**
     * Resets the current step
     */
    resetStep
  }
})
