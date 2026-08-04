import zod from 'zod'

// interface Player {
//   name: string
// }

// export interface Team {
//   id: string
//   name: string
//   players: Player[]
//   score: number
//   color: string | null
// }

export const PlayerSchema = zod.object({
  name: zod.string()
})

export const TeamSchema = zod.object({
  id: zod.string(),
  name: zod.string(),
  players: zod.array(PlayerSchema),
  score: zod.number(),
  color: zod.string().nullable()
})

export type Player = zod.infer<typeof PlayerSchema>

export type Team = zod.infer<typeof TeamSchema>
