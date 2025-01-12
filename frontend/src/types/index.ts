export * from './websocket_messages'

export type DifficultyLevels = 'All' | 'Easy' | 'Medium' | 'Semi-Pro' | 'Difficult' | 'Expert'

export type SongGenres = 'All' | 'Pop' | 'Electro' | 'Rock' | 'Rhythm and blues' | 'Rap' | 'Classical'

export interface Artist {
    id: number
    name: string
    spotify_id: string
    spotify_avatar: string
    genre: string
    created_on: string
}

export interface Song { 
    id: number
    name: string 
    genre: string 
    youtube: string
    youtube_id: string
    year: number
    video_id: string
    spotify_id: string
    artist: Artist
    spotify_avatar: string
    youtube_watch_link: string
    difficulty: number
    created_on: string
}

export interface ArtistSong extends Exclude<Artist, 'created_on'>{
    song_set: Exclude<Song, 'artist'>[]
}

interface Player {
    name: string
}

export interface Team {
    name: string
    players: Player[]
    score: number
    color: string | null
}

export interface CacheSession {
    songs: Song[]
    currentStep: number
    teams: Team[]
    settings: {
        rounds: number
        timeLimit: string | null
        pointValue: number
        songDifficultyBonus: boolean
        speedBonus: boolean
        soloMode: boolean 
        adminPlays: boolean
        difficultyLevel: DifficultyLevels
        songType: SongGenres
    }
}

export interface CreateData {
    name: string
    genre: string
    artist: string
    featured_artists: string | null
    youtube_id: string
    year: string | number | null
    difficulty: number
}

export interface Answer {
    teamId: number
    song: Song
}
