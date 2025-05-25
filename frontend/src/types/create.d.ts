/**
 * The data to be created in the database
 */
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
