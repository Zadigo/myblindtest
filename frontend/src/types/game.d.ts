import type { DifficultyLevels, MatchedPart, SongGenres } from '@/data/constants'
import type { Nullable, Song } from '.'

export type BlindtestPlayer = {
  id: string
  name: string
  color: string
  points: number
  team?: Nullable<string>
  correctAnswers: Arrayable<number>
  position: number
}

export interface CacheSession {
  songsPlayed: Song[]
  currentStep: number
  players: Record<string, BlindtestPlayer>
  settings: {
    rounds: number
    timeLimit: number
    pointValue: number
    songDifficultyBonus: boolean
    speedBonus: boolean
    soloMode: boolean
    adminPlays: boolean
    difficultyLevel: DifficultyLevels
    songType: SongGenres
    timeRange: number[]
    availableTeams: string[]
  }
}

/**
 * The team's anwswer given the current song
 */
export interface Answer {
  playerId: string
  matched: MatchedPart
  song: Song
}

export interface SettingsApiResponse {
  count_by_genre: GenreDistribution[]
  period: {
    minimum: number
    maximum: number
  }
}
