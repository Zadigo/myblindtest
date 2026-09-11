import type { _DatabaseItem, Nullable } from "."

export type GlobalSongGenres = 'pop' 
  | 'rock' 
  | 'hip-hop' 
  | 'jazz' 
  | 'classical' 
  | 'electronic'

export interface Artist extends _DatabaseItem {
  name: string
  spotify_id: string
  spotify_avatar: string
  genre: string
  wikipedia_page: Nullable<string>
}

export interface Song extends _DatabaseItem {
  name: string
  genre: string
  youtube: string
  youtube_id: string
  year: number
  video_id: string
  artist: Artist
  youtube_watch_link: string
  difficulty: number
}

type SongSet = Omit<Song, 'artist'>

export interface ArtistSong extends Exclude<Artist, 'created_on'> {
  song_set: SongSet[]
}

export interface GenreDistribution {
  genre: string
  count: number
}
