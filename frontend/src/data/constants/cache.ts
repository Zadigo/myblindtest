import type { CacheSession } from '@/types'

export const defaults: CacheSession = {
  songsPlayed: [],
  currentStep: 0,
  players: {},
  availableAnswers: [],
  playerAnswers: [],
  pendingScoresUpdate: {},
  settings: {
    rounds: 0,
    timeLimit: 0,
    pointValue: 1,
    songDifficultyBonus: false,
    speedBonus: false,
    soloMode: false,
    adminPlays: false,
    difficultyLevel: 'All',
    genreSelected: 'All',
    timeRange: [],
    multipleChoiceAnswers: false,
    pointLimit: 0,
  }
}
