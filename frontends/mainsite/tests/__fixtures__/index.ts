import type { CacheSession, BlindtestPlayer } from '../../app/types'
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
    difficultyLevel: 'medium',
    genreSelected: 'all',
    timeRange: [1900, 2024],
    multipleChoiceAnswers: true,
    pointLimit: 0
  }
}

export const playersFixture: BlindtestPlayer[] = [
  {
    id: faker.string.uuid(),
    name: faker.person.firstName(),
    color: faker.color.rgb(),
    points: faker.number.int(),
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
