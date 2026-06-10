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
