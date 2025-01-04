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
    color: string | null
}

export interface CacheSession {
    songs: Song[]
    currentStep: number
    teams: Team[]
    settings: {
        rounds: number
        timeLimit: number
        pointValue: number
        matchDifficulty: boolean
        difficultyLevel: 'All' | 'Easy' | 'Medium' | 'Difficult' | 'Expert'
        songType: 'All' | 'Pop' | 'Electro' | 'Rock'
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
    teamId: number
    song: Song
}
