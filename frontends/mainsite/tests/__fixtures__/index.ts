import type { CacheSession } from '../../app/types'

export const cachedSession: CacheSession = {
  songsPlayed: [],
  currentStep: 0,
  players: {},
  availableAnswers: [],
  playerAnswers: [],
  pendingScoresUpdate: {},
  settings: {
    adminPlays: false,
    rounds: 5,
    timeLimit: 30,
    pointValue: 100,
    songDifficultyBonus: false,
    speedBonus: false,
    soloMode: false,
    difficultyLevel: 'medium',
    genreSelected: 'all',
    timeRange: [1900, 2024],
    multipleChoiceAnswers: true,
    pointLimit: 0
  }
}
