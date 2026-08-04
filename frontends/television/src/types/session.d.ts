import { difficultyLevels } from '@/data/constants'
import { TeamSchema } from './game'
import { GlobalSongGenres, SongSchema } from './songs'
import zod from 'zod'

// export interface CacheSession {
//   songsPlayed: Song[]
//   currentStep: number
//   teams: Team[]
//   settings: {
//     rounds: number
//     timeLimit: string | null
//     pointValue: number
//     songDifficultyBonus: boolean
//     speedBonus: boolean
//     soloMode: boolean
//     adminPlays: boolean
//     difficultyLevel: DifficultyLevels
//     songType: GlobalSongGenres
//     timeRange: number[]
//   }
// }

export const CacheSessionSchema = zod.object({
  songsPlayed: zod.array(SongSchema),
  currentStep: zod.number(),
  teams: zod.array(TeamSchema),
  settings: zod.object({
    rounds: zod.number(),
    timeLimit: zod.string().nullable(),
    pointValue: zod.number(),
    songDifficultyBonus: zod.boolean(),
    speedBonus: zod.boolean(),
    soloMode: zod.boolean(),
    adminPlays: zod.boolean(),
    difficultyLevel: zod.enum(difficultyLevels),
    songType: zod.enum(GlobalSongGenres),
    timeRange: zod.array(zod.number())
  })
})

export type CacheSession = zod.infer<typeof CacheSessionSchema>
