import type { BlindtestPlayer, CacheSession, Song, Undefineable } from '@/types'

export * from './admin'
export * from './player'
export * from './utils'

export type WsSendMessage = { action: 'start_game' }
  | { action: 'stop_game' }
  | { action: 'not_guessed' }
  | { action: 'submit_guess', team_or_player_id: string, title_match: boolean, artist_match: boolean }
  | { action: 'game_settings', settings: Undefineable<CacheSession['settings']> }
  | { action: 'update_player', id: Undefineable<string>, name: string }

export type WsReceiveMessage = { action: 'device_accepted', player: BlindtestPlayer, players: Record<string, BlindtestPlayer> }
  | { action: 'device_disconnected', players: Record<string, BlindtestPlayer> }
  | { action: 'idle_connect', player: BlindtestPlayer }
  | { action: 'game_started' }
  | { action: 'song_new', song: Song }
  | { action: 'guess_correct', player_id: string, points: number, song: Song }
  | { action: 'guess_incorrect', player_id: string, points: number, song: Song }
  | { action: 'game_disconnected' }
  | { action: 'error', message: string }
  | { action: 'idle_response', code: number, connection_url: string }
  | { action: 'show_answer' }

