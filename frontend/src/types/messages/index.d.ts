import type { RandomizerData } from '@/components/randomizer'
import type { CacheSession } from '../game'
import type { GlobalSongGenres, Song } from '../songs'
import type { DefaultType } from '..'

export type CommonActions = 'error' | 'idle_connect' | 'check_code'

export type GroupActions = 'device_connected'
  | 'device_disconnected'
  | 'device_accepted'
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

export type _SendMessages = { action: 'idle_connect', firebase_key: string, settings: CacheSession }
  | { action: 'check_code', code: string }
  | { action: 'start_game' }
  | { action: 'submit_guess', team_id: number, title_match: Nullable<string>, artist_match: Nullable<string> }
  | { action: 'skip_song' }
  | { action: 'device_connected', device_id: string }
  | { action: 'device_disconnected', device_id: string }
  | { action: 'randomize_genre', temporary_genre: DefaultType<string | RandomizerData> }
  
  export type _ReceiveMessages = 
  | { action: 'idle_response', code: string }
  | { action: 'game_started' }
  | { action: 'game_complete', message: string, final_scores: { team_one: number, team_two: number }, songs_played: number }
  | { action: 'song_new', song: Song }
  | { action: 'timer_tick', remaining_time: number, total_time: number }
  | { action: 'guess_correct', team_id: number, points: number }
  | { action: 'guess_incorrect', team_id: number, points: number }
  | { action: 'device_accepted', device_id: string, message: string }
  | { action: 'error', message: string }

/**
 * Template message used to group diffusion messages
 * @deprecated
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

/**
 * @deprecated
 */
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
 * @deprecated
 */
export type WebsocketReceiveMessage = BaseWebsocketMessage & WebsocketGameComplete & {
  code: number
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
 * @deprecated
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
 * @deprecated
 */
export interface WebsocketSendGuess {
  team_id: string
  title_match: string | boolean | null
  artist_match: string | boolean | null
}

/**
 * Template message used to ask for a random music
 * based on the provided genre
 * @deprecated
 */
export interface WebsocketRandomizeGenre {
  temporary_genre: string | null | undefined | RandomizerData
}

/**
 * Template messages for messages that are sent from the client
 * to the Django
 * @deprecated
 */
export type WebsocketSendMessage = BaseWebsocketMessage | WebsocketRandomizeGenre | WebsocketInitializationMessage | WebsocketSendGuess | {
  exclude: number[]
  genre: GlobalSongGenres
}

/**
 * Send and receive messages over the websocket
 * @deprecated
 */
export type WebsocketMessage = WebsocketReceiveMessage & WebsocketSendMessage
