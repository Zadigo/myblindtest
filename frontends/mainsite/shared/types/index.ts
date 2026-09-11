import type { MATCHED_PART, DIFFICULTY_LEVELS, SONG_GENRES  } from '~/constants'

export type * from './create'
export type * from './game'
export type * from './songs'
export type * from './statistics'

export interface BaseApiResponse<T> {
  next: number
  previous: number
  results: T[]
}

export interface _DatabaseItem {
  id: number
  created_on: string
}

export type CustomLocationQuery = Partial<{ id: string, player: string }>

/**
 * Constants
 */

export type MatchedPart = (typeof MATCHED_PART)[ number ]

export type DifficultyLevels = (typeof DIFFICULTY_LEVELS)[ number ]

export type SongGenres = (typeof SONG_GENRES)[ number ]
