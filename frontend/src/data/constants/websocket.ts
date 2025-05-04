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
  'song_new',
  'timer_tick',
  'guess_correct',
  'error',
  'connection_token',
  'game_started',
  'song_skipped',
  'start_game',
  'submit_guess',
  'skip_song',
  'randomize_genre'
] as const

export type WebsocketActions = (typeof websocketActions)[number]
