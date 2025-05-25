import type { DifficultyLevels, SongGenres } from '../data/constants'

export * from './websocket_messages'
export * from './vue'

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
  artist: Artist
  youtube_watch_link: string
  difficulty: number
  created_on: string
}

export interface ArtistSong extends Exclude<Artist, 'created_on'> {
  song_set: Exclude<Song, 'artist'>[]
}

interface Player {
  name: string
}

export interface Team {
  id: number
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
    timeRange: number[]
  }
}

export interface CreateData {
  name: string
  genre: string
  artist_name: string
  featured_artists: string[]
  youtube_id: string
  year: number
  difficulty: number
}

export interface CopiedCreateData extends Omit<CreateData, 'featured_artists'> {
  featured_artists: string
}

export interface Answer {
  teamId: number
  matched?: 'Title' | 'Artist' | 'Both'
  song: Song
}

export interface GenreDistribution {
  genre: string
  count: number
}

export interface SettingsDataApiResponse {
  count_by_genre: GenreDistribution[]
  period: {
    minimum: number
    maximum: number
  }
}
