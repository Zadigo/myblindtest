import type { CacheSession } from '@/types'

export const defaults: CacheSession = {
  songs_played: [],
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
    timeLimit: null,
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
