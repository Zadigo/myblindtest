import type { DifficultyLevels, Song, SongGenres } from '@/types';
import type { RandomizerData } from '../components/randomizer';
import type { CacheSession } from '.';

export type MatchedElement = 'Artist' | 'Title' | 'Both' | null

type DeviceActions = 'device_connected' | 'device_disconnected' | 'update_device_cache' | 'apply_cache' | 'game_updates' | 'game_disconnected' | 'initiate_connection'

export type WebsocketActions = 'song_new' | 'timer_tick' | 'guess_correct' | 'error' | 'connection_token' | 'game_started' | 'song_skipped' | 'start_game' | 'submit_guess' | 'skip_song' | 'randomize_genre'

export interface WebsocketMessage {
    action: WebsocketActions | DeviceActions
}

export interface WebsocketBlindTestMessage extends WebsocketMessage {
    // Received
    token?: string | null | undefined,
    song?: Song
    team?: number
    points?: number
    error?: string

    // Send
    cache?: CacheSession
    exclude?: number[]
    genre?: SongGenres
    temporary_genre?: string | null | undefined | RandomizerData

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

export interface WebsocketDiffusionMessage {
    action: DeviceActions
    cache?: CacheSession
    device_id?: string
    updates?: {
        action: Pick<WebsocketMessageTypes, 'guess_correct'>
        team_id: number,
        points: number
    }
}
