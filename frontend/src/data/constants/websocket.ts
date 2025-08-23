export const matchedPart = [
  'Artist',
  'Title',
  'Both'
] as const

export type MatchedPart = (typeof matchedPart)[number]
