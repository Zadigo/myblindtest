import type { Song } from '.'
import type { DifficultyLevels, MatchedPart, SongGenres } from '../data/constants'

interface Player {
  name: string
}

export interface Team {
  id: string
  name: string
  players: Player[]
  score: number
  color: string | null
}

export interface CacheSession {
  songs: Song[] // TODO: Rename to previous_songs or songs_played

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

export interface SettingsDataApiResponse {
  count_by_genre: GenreDistribution[]
  period: {
    minimum: number
    maximum: number
  }
}

export interface VideoBlockExposedMethods {
  handleCorrectAnswer: (teamId: string, match: MatchedPart) => void
  handleIncorrectAnswer: () => void
}
