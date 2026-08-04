import { describe, it, expect, vi } from 'vitest'
import VideoBlock from '../../../app/components/blindtest/VideoBlock.vue'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { cachedSession } from '../../__fixtures__'

vi.mock('../../../app/composables/use/session', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../../../app/composables/use/session.ts')>()
  return {
    ...actual,
    useSession: vi.fn(() => {
      return {
        currentSettings: ref(cachedSession)
      }
    })
  }
})

const mockedAdminWebsocket = vi.fn(() => {
  return {
    gameStarted: ref(false),
    wsObject: vi.fn(),
    isConnected: ref(false),
    blindTestDoc: ref({}),
    players: ref([]),
  }
})

vi.mock('../../../app/composables/use/game/wsmanagers/admin', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../../../app/composables/use/game/wsmanagers/admin')>()
  return {
    ...actual,
    useAdminWebsocket: vi.fn(() => mockedAdminWebsocket())
  }
})

describe('VideoBlock', () => {
  it('should render the video block correctly', async () => {
    const component = await mountSuspended(VideoBlock)

    // console.log(component.html())
  })
})
