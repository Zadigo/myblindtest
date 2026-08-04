import zod from 'zod'

// export interface Artist {
//   id: number
//   name: string
//   spotify_id: string
//   spotify_avatar: string
//   genre: string
//   created_on: string
// }

// export interface Song {
//   id: number
//   name: string
//   genre: string
//   featured_artists: string[]
//   youtube: string
//   youtube_id: string
//   year: number
//   youtube_watch_link: string
//   artist_name: string
//   artist: Artist
//   difficulty: number
//   created_on: string
// }

export const ArtistSchema = zod.object({
  id: zod.number(),
  name: zod.string(),
  spotify_id: zod.string(),
  spotify_avatar: zod.string(),
  genre: zod.string(),
  created_on: zod.string()
})

export const SongSchema = zod.object({
  id: zod.number(),
  name: zod.string(),
  genre: zod.string(),
  featured_artists: zod.array(zod.string()),
  youtube: zod.string(),
  youtube_id: zod.string(),
  year: zod.number(),
  youtube_watch_link: zod.string(),
  artist_name: zod.string(),
  artist: ArtistSchema,
  difficulty: zod.number(),
  created_on: zod.string()
})

export type Artist = zod.infer<typeof ArtistSchema>

export type Song = zod.infer<typeof SongSchema>
