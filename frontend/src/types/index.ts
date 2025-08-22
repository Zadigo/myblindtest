export type * from './messages'
export type * from './create'
export type * from './game'
export type * from './vue'

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

export interface GenreDistribution {
  genre: string
  count: number
}
