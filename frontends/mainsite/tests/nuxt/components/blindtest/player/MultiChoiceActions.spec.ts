import { describe, it, vi, expect } from 'vitest'
import MultiChoiceActions from '../../../../../app/components/blindtest/player/MultiChoiceActions.vue'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { cachedSession } from '../../../../__fixtures__'
// import { useSound } from '@vueuse/sound'

// const { mockedPlay, _mockedUserPlayerSession } = vi.hoisted(() => {
//   return {
//     mockedPlay: vi.fn(),
//     mockedUserPlayerSession: {
//       id: 'session-123',
//       status: 'active'
//     }
//   }
// })

// const mockedUserPlayerSession = vi.fn().mockReturnValue({
//   currentSettings: ref(cachedSession)
// })

// vi.mock('../../../../../app/composables/use/session', async (importOriginal) => {
// const actual = await importOriginal<typeof import('../../../../../app/composables/use/session')>()
//   return {
//     ...actual,
//     usePlayerSession: mockedUserPlayerSession
//   }
// })

// const mockPlay = vi.fn()

// vi.mock('@vueuse/sound', () => ({
//   useSound: vi.fn(() => ({
//     play: mockPlay,
//     stop: vi.fn(),
//     pause: vi.fn(),
//     isPlaying: { value: false },
//   })),
// }))

describe.todo('MultiChoiceActions', () => {
  it('should render the multi choice actions correctly', async () => {
    const component = await mountSuspended(MultiChoiceActions)

    // console.log(component.html())
  })
})
