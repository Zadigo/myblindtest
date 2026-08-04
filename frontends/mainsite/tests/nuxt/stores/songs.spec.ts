import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia, storeToRefs } from 'pinia'
import { useSongs  } from '~/stores/songs'

describe('Songs Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initializes correctly', () => {
    const songsStore = useSongs()
    const { currentStep, answers, correctAnswers, scoringTimelineBase, songsPlayed, scoringTimeline  } = storeToRefs(songsStore)
    
    expect(toValue(currentStep)).toBe(0)
    expect(toValue(answers)).toEqual([])
    expect(toValue(correctAnswers)).toEqual([])
    expect(toValue(scoringTimelineBase)).toBe(100)
    expect(toValue(scoringTimeline)).toEqual([])
    expect(toValue(songsPlayed)).toEqual([])
  })
})
