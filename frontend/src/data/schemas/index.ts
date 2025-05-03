import { z } from 'zod'
import { difficultyLevels, songGenres } from '../constants'

export const addNewSongData = z.object({
  name: z.string().nullable(),
  genre: z.enum(songGenres),
  artist_name: z.string().nullable(),
  featured_artists: z.string().array(),
  youtube_id: z.string(),
  year: z.number(),
  difficulty: z.number().default(1)
})

export type AddNewSongData = z.infer<typeof addNewSongData>

export const Team = z.object({
  id: z.number(),
  name: z.string().nullable(),
  score: z.number().default(0),
  players: z.string().array(),
  color: z.string().nullable()
})

export const Settings = z.object({
  rounds: z.number().default(1),
  timeLimit: z.number(),
  pointValue: z.number().default(1),
  songDifficultyBonus: z.boolean(),
  speedBonus: z.boolean(),
  soloMode: z.boolean(),
  adminPlays: z.boolean(),
  difficultyLevel: z.enum(difficultyLevels),
  songType: z.enum(songGenres),
  timeRange: z.number().array()
})

export const sessionData = z.object({
  cache: z.object({
    songs: z.string().array(),
    currentStep: z.number().default(0),
    teams: Team.array(),
    settings: Settings
  })
})

export type SessionData = z.infer<typeof sessionData>
