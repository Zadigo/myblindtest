import type { RandomizerData } from '@/components/randomizer'
import type { Song, SongGenres } from '@/types'
import type { CacheSession } from '../game'

export type CommonActions = 'error' | 'idle_connect' | 'check_code'

export type GroupActions = 'device_connected'
  | 'device_disconnected'
  | 'update_device_cache'
  | 'game_updates'
  | 'game_disconnected'
  

export type GameActions = 'start_game'
  | 'game_started'
  | 'game_complete'
  | 'song_new'
  | 'guess_correct'
  | 'guess_incorrect'
  | 'randomize_genre'
  | 'timer_tick'
  | 'song_skipped'
  | 'submit_guess'
  | 'skip_song'

export type DefaultActions = CommonActions | GameActions | GroupActions

export interface BaseWebsocketMessage {
  action: DefaultActions
  message: string
}

/**
 * Template message used to group diffusion messages
 */
export interface WebsocketGroupDiffusionMessage {
  action: GroupActions
  cache: CacheSession
  device_id: string
  updates: {
    action: Pick<WebsocketMessageTypes, 'guess_correct'>
    team_id: number
    points: number
  }
}

export interface WebsocketGameComplete {
  /**
   * Final scores for each team when
   * "game_complete" action is received
   */
  final_scores: {
    team_one: number
    team_two: number
  }
  /**
   * Songs played during the game when
   * "game_complete" action is received
   */
  songs_played: Song[]
}

/**
 * Template messages that used to receive messages from Django
 */
export type WebsocketReceiveMessage = BaseWebsocketMessage & WebsocketGameComplete & {
  code: string
  /**
   * Whether the code check was valid
   */
  valid: boolean
  /**
   * New song to guess
   */
  song: Song
  team: number // TODO: Remove
  /**
   * Updated team points
   */
  points: number
  /**
   * ID of the team being updated
   */
  team_id: string
}

/**
 * Sends the settings from the cache to Django
 */
export interface WebsocketInitializationMessage {
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

/**
 * Template message used to send a guess to a song
 */
export interface WebsocketSendGuess {
  team_id: string
  title_match: string | boolean | null
  artist_match: string | boolean | null
}

/**
 * Template message used to ask for a random music
 * based on the provided genre
 */
export interface WebsocketRandomizeGenre {
  temporary_genre: string | null | undefined | RandomizerData
}

/**
 * Template messages for messages that are sent from the client
 * to the Django
 */
export type WebsocketSendMessage = BaseWebsocketMessage | WebsocketRandomizeGenre | WebsocketInitializationMessage | WebsocketSendGuess | {
  exclude: number[]
  genre: SongGenres
}

/**
 * Send and receive messages over the websocket
 */
export type WebsocketMessage = WebsocketReceiveMessage & WebsocketSendMessage
