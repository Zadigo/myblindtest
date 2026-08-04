import GuessState from '../../../../../app/components/blindtest/score/GuessState.vue'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect } from 'vitest'
import type { Song } from '~/types'
import { songsFixture } from '../../../../__fixtures__'

type TestCase = {
  correctSong: Song | null | undefined
  isCorrectGuess: boolean
  isIncorrectGuess: boolean
  expectedImage: boolean
  expectedTitleText: boolean
  caseText: string
}

const testCases: TestCase[] = [
  {
    correctSong: songsFixture[0],
    isCorrectGuess: false,
    isIncorrectGuess: false,
    expectedImage: true,
    expectedTitleText: true,
    caseText: 'correctSong is defined, isCorrectGuess and isIncorrectGuess are false'
  },
  {
    correctSong: null,
    isCorrectGuess: false,
    isIncorrectGuess: false,
    expectedImage: false,
    expectedTitleText: false,
    caseText: 'correctSong is null, isCorrectGuess and isIncorrectGuess are false'
  },
  {
    correctSong: songsFixture[0],
    isCorrectGuess: true,
    isIncorrectGuess: false,
    expectedImage: true,
    expectedTitleText: true,
    caseText: 'correctSong is defined, isCorrectGuess is true and isIncorrectGuess is false'
  },
  {
    correctSong: songsFixture[0],
    isCorrectGuess: true,
    isIncorrectGuess: true,
    expectedImage: true,
    expectedTitleText: true,
    caseText: 'correctSong is defined, isCorrectGuess and isIncorrectGuess are true'
  },
]

describe('GuessState', () => {
  testCases.forEach(({ caseText, correctSong, isCorrectGuess, isIncorrectGuess, expectedImage, expectedTitleText }) => {
    it(caseText, async () => {
      const component = await mountSuspended(GuessState, {
        props: {
          // @ts-ignore
          correctSong,
          isCorrectGuess,
          isIncorrectGuess
        }
      })
  
      const imageEl = component.find('img')
      expect(imageEl.exists()).toBe(expectedImage)

      const titles: string[] = ['h1', 'h2', 'h3']
      
      titles.forEach((tag) => {
        const titleEl = component.find(tag)
        expect(titleEl.exists()).toBe(true)
      })

      if (!expectedTitleText) {
        titles.filter(tag => tag !== 'h1').forEach((tag) => {
          const titleEl = component.find(tag)
          expect(titleEl.text()).toEqual('')
        })
      }

      if (isCorrectGuess && !isIncorrectGuess) {
        const titleEl = component.find('h1')
        expect(titleEl.text()).toEqual('Good answer!')
      }

      if (!isCorrectGuess && isIncorrectGuess) {
        const titleEl = component.find('h1')
        expect(titleEl.text()).toEqual('Wrong answer!')
      }

      if (isCorrectGuess && isIncorrectGuess) {
        const titleEl = component.find('h1')
        expect(titleEl.text()).toEqual('No answers given')
      }
    })
  })
})
