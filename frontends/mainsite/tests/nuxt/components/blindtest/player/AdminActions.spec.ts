import { describe, it, expect, vi } from 'vitest'
import AdminActions from '../../../../../app/components/blindtest/player/AdminActions.vue'
import { mountSuspended } from '@nuxt/test-utils/runtime'

const mockedAdminWebsocket = vi.fn(() => {
  return {
    gameStarted: ref(false),
    wsObject: vi.fn(),
    isConnected: ref(false),
    blindTestDoc: ref({}),
    players: ref([]),
  }
})

vi.mock('../../../../../app/composables/use/game/wsmanagers/admin', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../../../../../app/composables/use/game/wsmanagers/admin')>()
  return {
    ...actual,
    useAdminWebsocket: vi.fn(() => mockedAdminWebsocket())
  }
})

describe('AdminActions', () => {
  it('should render the admin actions correctly', async () => {
    const component = await mountSuspended(AdminActions)

    // console.log(component.html())
  })
})
