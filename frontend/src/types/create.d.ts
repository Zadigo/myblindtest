type ArtistName = string | { label: string; value: string }


/**
 * The data to be created in the database
 */
export interface NewSong {
  name: string
  genre: string
  artist_name: ArtistName
  featured_artists: string[]
  youtube_id: string
  year: number
  difficulty: number
}

export type CopiedCreateData = Omit<NewSong, 'featured_artists'>
