export const difficultyLevels = [
  'All',
  'Easy',
  'Medium',
  'Semi-Pro',
  'Difficult',
  'Expert'
] as const

export type DifficultyLevels = (typeof difficultyLevels)[number]

export const songGenres = [
  'All',
  'Pop',
  'Electro',
  'Rock',
  'Rhythm and blues',
  'Rap',
  'Classical'
] as const

export type SongGenres = (typeof songGenres)[number]
