import type { CacheSession } from '@/types'

export const defaults: CacheSession = {
  songsPlayed: [],
  currentStep: 0,
  teams: [
    {
      id: '1',
      name: '',
      score: 0,
      players: [],
      color: null
    },
    {
      id: '2',
      name: '',
      score: 0,
      players: [],
      color: null
    }
  ],
  settings: {
    rounds: 1,
    timeLimit: 0,
    pointValue: 1,
    songDifficultyBonus: false,
    speedBonus: false,
    soloMode: false,
    adminPlays: false,
    difficultyLevel: 'All',
    songType: 'All',
    timeRange: []
  }
}
