type AutoCompleteReturn = { label: string; value: string }

type ArtistName = string | AutoCompleteReturn

type GenreName = string | Pick<AutoCompleteReturn, 'label'>

/**
 * The data to be created in the database
 */
export interface NewSong {
  name: string
  genre: GenreName,
  artist_name: ArtistName
  featured_artists: string[]
  youtube_id: string
  year: number
  difficulty: number
  is_group: boolean,
  wikipedia_page?: string
}

export type CopiedCreateData = Omit<NewSong, 'featured_artists'>
