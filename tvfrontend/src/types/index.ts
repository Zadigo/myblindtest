export type DefaultActions = 'idle_connect' | 'check_code' | 'game_updates' | 'game_disconnected'

export interface BaseWebsocketMessage {
  action: DefaultActions
}

export interface WebsocketSendMessage extends BaseWebsocketMessage {
  pinCode: number
}

export interface WebsocketReceiveMessage extends BaseWebsocketMessage {
  optChallengeResult: boolean
  valid: boolean
}

export type WebsocketMessage = WebsocketSendMessage & WebsocketReceiveMessage
