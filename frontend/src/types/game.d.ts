import type { DifficultyLevels, MatchedPart, SongGenres } from '@/data/constants'
import type { Nullable, Song } from '.'

interface Player {
  name: string
}

export interface Team {
  id: string
  name: string
  players: Player[]
  score: number
  color: Nullable<string>
}

export interface CacheSession {
  songsPlayed: Song[]
  currentStep: number
  teams: Team[]
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
  }
}

/**
 * The team's anwswer given the current song
 */
export interface Answer {
  teamId: string
  matched?: MatchedPart
  song: Song
}

export interface SettingsApiResponse {
  count_by_genre: GenreDistribution[]
  period: {
    minimum: number
    maximum: number
  }
}

export interface VideoBlockExposedMethods {
  sendCorrectAnswer: (teamId: string, match: MatchedPart) => void
  sendIncorrectAnswer: () => void
}
