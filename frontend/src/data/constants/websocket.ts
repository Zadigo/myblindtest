export const matchedElement = [
  'Artist',
  'Title',
  'Both',
  null
] as const

export type MatchedElement = (typeof matchedElement)[number]

export const deviceActions = [
  'device_connected',
  'device_disconnected',
  'update_device_cache',
  'apply_cache',
  'game_updates',
  'game_disconnected',
  'initiate_connection'
] as const

export type DeviceActions = (typeof deviceActions)[number]

export const websocketActions = [
  'connection_token',
  'error',
  'guess_correct',
  'game_started',
  'randomize_genre',
  'song_new',
  'timer_tick',
  'song_skipped',
  'start_game',
  'submit_guess',
  'skip_song'
] as const

export type WebsocketActions = (typeof websocketActions)[number]
