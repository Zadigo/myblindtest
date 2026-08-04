import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useGameCountdown} from '~/composables/use/game/countdown'
import { mountSuspended } from '@nuxt/test-utils/runtime'

const mockedUseAdminWebsocket = vi.fn().mockReturnValue({
  gameStarted: ref(false)
})

vi.mock('~/composables/use/game/wsmanagers/admin', async (originlImport) => {
  const actual = await originlImport<typeof import('~/composables/use/game/wsmanagers/admin')>()

  return {
    ...actual,
    useAdminWebsocket: vi.fn(() => mockedUseAdminWebsocket())
  }
})

describe('useGameCountdown', { tags: ['composable'] }, () => {
  it('should initialize countdown timer with correct time limit', () => {
    const result = useGameCountdown()

    const expectedProperties = [
      'remaining',
      'isActive',
      'timerToMinutes',
      'timeLimit',
      'hasTimer',
      'lessThanFiveSeconds',
      'lessThanTenSeconds',
      'restart'
    ]

    expectedProperties.forEach((item) => {
      expect(result).toHaveProperty(item)
    })

    expect(result.restart).toBeInstanceOf(Function)
  })
})

describe('useGameCountdown Implemntation', { tags: ['composable'] }, () => {
  let mockTemplate: ReturnType<typeof defineComponent> | undefined

  beforeEach(() => {
    mockTemplate = defineComponent({
      template: `
      <div>
        {{ gameStarted }}
      </div>
      `,
      setup() {
        const { gameStarted } = useAdminWebsocket()
        return { gameStarted }
      }
    })
  })

  it('should start countdown when gameStarted is true', async () => {
    const wrapper = await mountSuspended(mockTemplate)
    console.log(wrapper.html())
  })
})
