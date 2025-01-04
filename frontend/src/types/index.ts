export interface Song { 
    id: number
    name: string 
    genre: string 
    artist: string 
    youtube: string
    year: number
    video_id: string
    youtube_watch_link: string
    difficulty: number
    created_on: string
}

interface Player {
    name: string
}

export interface Team {
    name: string
    players: Player[]
    score: number
    color: string
}

export interface CacheSession {
    songs: Song[]
    currentStep: number
    teams: Team[]
    settings: {
        rounds: number
        timeLimit: number
    }
}

export interface CreateData {
    name: string
    genre: string,
    artist: string
    youtube: string
    year: string | number | null
}

export interface Answer {
    song: Song
}
