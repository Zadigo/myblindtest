import { DifficultyLevels } from '@/data/constants'
import { Team } from "./game"
import { GlobalSongGenres, Song } from './songs'

export interface CacheSession {
  songsPlayed: Song[]
  currentStep: number
  teams: Team[]
  settings: {
    rounds: number
    timeLimit: string | null
    pointValue: number
    songDifficultyBonus: boolean
    speedBonus: boolean
    soloMode: boolean
    adminPlays: boolean
    difficultyLevel: DifficultyLevels
    songType: GlobalSongGenres
    timeRange: number[]
  }
}
