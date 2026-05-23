import type { Song } from '@/types'

export const useGameStore = defineStore('game', () => {
  const correctAnswerTeamId = refAutoReset<string | undefined>(undefined, 6000)
  const showAnswer = refAutoReset<boolean>(false, 5000)
  const answer = refAutoReset<Song | null>(null, 5000)

  return {
    correctAnswerTeamId,
    answer,
    showAnswer
  }
})
