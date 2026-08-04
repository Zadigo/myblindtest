import MainCard from '../../../../../app/components/blindtest/score/MainCard.vue'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect } from 'vitest'
import type { BlindtestPlayer } from '../../../../../app/types'
import { playersFixture } from '../../../../__fixtures__'

type TestCase = {
  player: BlindtestPlayer | undefined,
  isReady: boolean,
  expected: boolean
}

const testCases: TestCase[] = [
  {
    player: playersFixture[0],
    isReady: true,
    expected: true
  },
  {
    player: playersFixture[1],
    isReady: false,
    expected: false
  },
  {
    player: undefined,
    isReady: true,
    expected: false
  }
]

describe('MainCard', () => {
  testCases.forEach(({ player, isReady, expected }) => {
    it(`should render the main card correctly when isReady is ${isReady} and player ${player?.name}`, async () => {
      const component = await mountSuspended(MainCard, {
        props: {
          player,
          isReady,
        }
      })

      console.log(component.html())
      
      const titleEl = component.find('h1')
      expect(titleEl.exists()).toBe(expected)
    })
  })


  it('should emit toggle-settings-modal event when the button is clicked', async () => {
    const component = await mountSuspended(MainCard, {
      props: {
        player: playersFixture[0],
        isReady: true,
      }
    })

    const buttonEl = component.find('button')
    await buttonEl.trigger('click')

    expect(component.emitted()).toHaveProperty('toggle-settings-modal')
  })
})
