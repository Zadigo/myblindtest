import { useConsecutiveAnswers } from '~/composables/use/game/answers'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { staticPlayerFixture, songsFixture } from '../../__fixtures__'
import type { Answer } from '~/types'

const { mockedStoreToRefs  } = vi.hoisted(() => {
  return {
    mockedStoreToRefs: vi.fn()
  }
})

vi.mock('pinia', async (originalImport) => {
  const actual = await originalImport<typeof import('pinia')>()
  return {
    ...actual,
    storeToRefs: mockedStoreToRefs.mockReturnValue({
      correctAnswers: ref<Answer[]>([])
    })
  }
})

describe.only('useConsecutiveAnswers', () => {
  const player = computed(() => staticPlayerFixture)
  const simpleCallbackSpy = vi.fn()

  it('should return default values', () => {
    const composable = useConsecutiveAnswers(player, undefined, 2)
    expect(composable).toHaveProperty('consecutiveAnswers')
    expect(composable).toHaveProperty('hasConsecutiveAnswers')

    expect(toValue(composable.consecutiveAnswers)).toEqual(0)
    expect(toValue(composable.hasConsecutiveAnswers)).toBeFalsy()

    // Consecutive answers should be 0 if player is undefined
    // player.value = undefined
    // expect(toValue(composable.consecutiveAnswers)).toEqual(0)
  })

  it('should return the amount of consecutive answers', () => {
    mockedStoreToRefs.mockReturnValue({
      correctAnswers: ref<Answer[]>(
        [
          {
            matched: 'Title',
            playerId: staticPlayerFixture.id,
            // @ts-ignore
            song: songsFixture[0]
          },
          {
            matched: 'Artist',
            playerId: staticPlayerFixture.id,
            // @ts-ignore
            song: songsFixture[0]
          },
          {
            matched: 'Title',
            playerId: staticPlayerFixture.id,
            // @ts-ignore
            song: songsFixture[0]
          },
          {
            matched: 'Artist',
            playerId: staticPlayerFixture.id,
            // @ts-ignore
            song: songsFixture[0]
          }
        ]
      )
    })

    const composable = useConsecutiveAnswers(player, simpleCallbackSpy, 2)
    
    expect(composable.hasConsecutiveAnswers).toBeTruthy()
    expect(toValue(composable.consecutiveAnswers)).toEqual(4)
    // expect(simpleCallbackSpy).toHaveBeenCalled()
    // expect(simpleCallbackSpy).toHaveBeenCalledTimes(1)
  })
})
