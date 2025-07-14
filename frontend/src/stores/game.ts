import type { Answer } from '@/types'

export const useGameStore = defineStore('game', () => {
  const songStore = useSongs()
  const { cache } = storeToRefs(songStore)

  const gameStarted = ref<boolean>(false)

  const firstTeamScore = computed(() => cache.value.teams[0].score)
  const secondTeamScore = computed(() => cache.value.teams[1].score)

  const answers = reactive<Answer[]>([])
  const correctAnswers = reactive<Answer[]>([])
  const incorrectAnswers = reactive<Answer[]>([])
  
  return {
    /**
     * Returns whether the game has started
     */
    gameStarted,
    /**
     * Returns the current song on which the
     */
    firstTeamScore,
    /**
     * Returns the score of the second team
     */
    secondTeamScore,
    /**
     * Returns the list of answers given by the players
     */
    answers,
    /**
     * Returns the list of correct answers
     */
    correctAnswers,
    /**
     * Returns the list of incorrect answers
     */
    incorrectAnswers
  }
})
