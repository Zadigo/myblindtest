import type { RandomizerData } from '@/components/randomizer'
import type { DeviceActions, WebsocketActions } from '@/data/constants/websocket'
import type { DifficultyLevels, Song, SongGenres } from '@/types'
import type { CacheSession } from '../game'

export type DefaultActions = WebsocketActions | DeviceActions

export interface BaseWebsocketMessage {
  action: DefaultActions
}

/**
 * Sends the settings from the cache to Django
 */
export interface WebsocketInitializationMessage extends BaseWebsocketMessage {
  action: DefaultActions
  /**
   * The Firebase key for other clients to
   * be able to connect to the database session
   */
  firebase_key: string
  /**
   * The session as registered in the Firebase
   * database and stored on Django
   */
  session: CacheSession
}

export interface WebsocketSendGuess extends BaseWebsocketMessage {
  team_id: string
  title_match: boolean
  artist_match: boolean
}

export interface WebsocketRandomizeGenre extends BaseWebsocketMessage {
  temporary_genre: string | RandomizerData
}

export type WebsocketReceiveMessage = BaseWebsocketMessage & {
  token?: string | null | undefined
  song?: Song
  team?: number
  points?: number
  error?: string
  team_one_id?: string
  team_two_id?: string
}

export type WebsocketSendMessage = BaseWebsocketMessage & {
  exclude?: number[]
  genre?: SongGenres
  temporary_genre?: string | null | undefined | RandomizerData

  team_id?: string
  title_match?: string | boolean | null
  artist_match?: string | boolean | null

  settings?: {
    point_value: number
    game_difficulty: DifficultyLevels
    genre: SongGenres
    difficulty_bonus: boolean
    time_bonus: boolean
    number_of_rounds: number
    solo_mode: boolean
    admin_plays: boolean
    teams?: {
      one: {
        name: string
      }
      two: {
        name: string
      }
    }
  }
}

export type WebsocketMessage = WebsocketReceiveMessage & WebsocketSendMessage

export interface WebsocketDiffusionMessage {
  action: DeviceActions
  cache?: CacheSession
  device_id?: string
  updates?: {
    action: Pick<WebsocketMessageTypes, 'guess_correct'>
    team_id: number
    points: number
  }
}
