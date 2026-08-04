import type { CacheSession } from '~/types'

export const MATCHED_PART = [
  'Artist',
  'Title',
  'Both'
] as const

export const DIFFICULTY_LEVELS = [
  'All',
  'Easy',
  'Medium',
  'Semi-Pro',
  'Difficult',
  'Expert'
] as const

export const SONG_GENRES = [
  'All',
  'Pop',
  'Electro',
  'Rock',
  'Rhythm and blues',
  'Rap',
  'Classical'
] as const

export const defaultCacheOptions: Readonly<CacheSession> = {
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
