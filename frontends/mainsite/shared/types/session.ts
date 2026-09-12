import type { BlindtestPlayer } from './game'

export type SessionApiResponse = {
  sessionId: string
}

export interface PlayerAnswer {
  player_id: string
  answer_index: number
}

export interface MultiChoiceAnswer {
  id: number
  name: string
  artist__name: string
  is_correct_answer: boolean
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
  genreSelected: SongGenres
  timeRange: number[]
  multipleChoiceAnswers: boolean
  pointLimit: number
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
