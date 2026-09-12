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
