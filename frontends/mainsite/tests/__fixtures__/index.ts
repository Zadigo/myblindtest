import type { CacheSession, BlindtestPlayer, Song } from '../../app/types'
import { faker } from '@faker-js/faker'

export const cachedSession: CacheSession = {
  songsPlayed: [],
  currentStep: 0,
  players: {},
  availableAnswers: [],
  playerAnswers: [],
  pendingScoresUpdate: {},
  settings: {
    adminPlays: false,
    rounds: 5,
    timeLimit: 30,
    pointValue: 100,
    songDifficultyBonus: false,
    speedBonus: false,
    soloMode: false,
    difficultyLevel: 'All',
    genreSelected: 'All',
    timeRange: [1900, 2024],
    multipleChoiceAnswers: true,
    pointLimit: 0
  }
}

export const staticPlayerFixture: BlindtestPlayer = {
  id: '1',
  name: 'Pauline',
  color: faker.color.rgb(),
  points: faker.number.int(),
  team: null,
  correctAnswers: [],
  position: faker.number.int({ min: 1, max: 10 }),
  speciality: null,
} 

export const playersFixture: BlindtestPlayer[] = [
  {
    id: faker.string.uuid(),
    name: faker.person.firstName(),
    color: faker.color.rgb(),
    points: faker.number.int({ min: 1, max: 10 }),
    team: null,
    correctAnswers: [],
    position: faker.number.int(),
    speciality: null,
  },
  {
    id: faker.string.uuid(),
    name: faker.person.firstName(),
    color: faker.color.rgb(),
    points: faker.number.int(),
    team: null,
    correctAnswers: [],
    position: faker.number.int(),
    speciality: null,
  }
]

export const songsFixture: Song[] = [
  {
    id: faker.number.int(),
    name: faker.music.songName(),
    genre: faker.music.genre(),
    youtube_id: faker.string.uuid(),
    year: faker.number.int({ min: 1900, max: 2024 }),
    video_id: faker.string.uuid(),
    youtube: `https://www.youtube.com/watch?v=${faker.string.uuid()}`,
    youtube_watch_link: `https://www.youtube.com/watch?v=${faker.string.uuid()}`,
    difficulty: faker.number.int({ min: 1, max: 5 }),
    artist: {
      id: faker.number.int(),
      name: faker.person.fullName(),
      spotify_id: faker.string.uuid(),
      spotify_avatar: faker.image.url({ width: 100, height: 100 }),
      genre: faker.music.genre(),
      wikipedia_page: null,
      created_on: new Date().toISOString()
    },
    created_on: new Date().toISOString()
  }
]
