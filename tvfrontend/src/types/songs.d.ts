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
  featured_artists: string[]
  youtube: string
  youtube_id: string
  year: number
  youtube_watch_link: string
  artist_name: string
  artist: Artist
  difficulty: number
  created_on: string
}
