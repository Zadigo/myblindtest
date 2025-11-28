import type { DifficultyLevels, MatchedPart, SongGenres } from '@/data/constants'
import type { Arrayable, Nullable, Song } from '.'

export type BlindtestPlayer = {
  id: string
  name: string
  color: string
  points: number
  team: Nullable<string>
  correctAnswers: Arrayable<number>
  position: number
  speciality: Nullable<string>
}

interface GameSettings {
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
  multipleChoiceAnswers: boolean
  pointLimit: number
}

export interface PlayerAnswer {
  player_id: string
  answer_index: number
}

export interface CacheSession {
  songsPlayed: Song[]
  currentStep: number
  players: Record<string, BlindtestPlayer>
  // TODO: Rename to possibilities
  availableAnswers: Arrayable<MultiChoiceAnswer>
  playerAnswers: Arrayable<PlayerAnswer>
  pendingScoresUpdate: Record<string, BlindtestPlayer>
  settings: GameSettings
}

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

export interface MultiChoiceAnswer {
  id: number
  name: string
  artist__name: string
  is_correct_answer: boolean
}
