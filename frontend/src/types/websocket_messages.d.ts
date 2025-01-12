import type { DifficultyLevels, Song, SongGenres } from '@/types';

export type WebsocketMessageTypes = 'song.new' | 'timer.tick' | 'guess.correct' | 'error' | 'connection.token' | 'game.started' | 'song.skipped' | 'start.game' | 'submit.guess' | 'skip.song' | 'randomize.genre'

// TODO: Create two different websocket types
// interface WebsocketReceiveMessage {
// }

// interface WebsocketSendMessage {
//   type
// }

export type MatchedElement = 'Artist' | 'Title' | 'Both' | null

export interface WebsocketMessage {
    type: WebsocketMessageTypes

    // Received
    token?: string | null | undefined,
    song?: Song
    team?: number
    points?: number

    // Send
    exclude?: number[]
    genre?: SongGenres

    team_id?: number
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
            },
            two: {
                name: string
            }
        }
    }
}
