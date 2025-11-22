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

export type IndividualBlindTestPlayer = {
  name: string
  color: string
  points: number
  correct_answers: Arrayable<number>
}

export interface CacheSession {
  songsPlayed: Song[]
  currentStep: number
  teams: Team[]
  players: Record<string, IndividualBlindTestPlayer>
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
  teamId: string // Rename to teamOrPlayerId
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
