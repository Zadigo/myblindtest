/**
 * The data to be created in the database
 * @todo Rename to NewSong
 */
export interface NewSong {
  name: string
  genre: string
  artist_name: string
  featured_artists: string[]
  youtube_id: string
  year: number
  difficulty: number
}

export type CopiedCreateData = Omit<NewSong, 'featured_artists'>
