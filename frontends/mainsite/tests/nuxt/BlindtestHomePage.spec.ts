import { describe, it, expect, vi } from 'vitest'
import BlindtestHome from '../../app/pages/blindtest/index.vue'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { mockNuxtImport } from '@nuxt/test-utils/runtime'
import { playersFixture } from '../__fixtures__'

mockNuxtImport('useRuntimeConfig', () => ({
  public: {
    wsUrl: 'ws://localhost:3000',
  }
}))

// vi.stubGlobal('useRouter', vi.fn())
// mockNuxtImport('useRouter', () => ({

// }))
// vi.mock('useRouter', () => ({
//   useRouter: () => ({
//     push: vi.fn(),
//   })
// }))

const t = vi.fn((key: string) => key)

vi.mock('i18n', () => ({
  useI18n: () => ({
    t,
    locale: ref('fr'),
  })
}))

vi.mock('../../app/composables/use/game/wsmanagers/admin', async (originalImport) => {
  const actual = await originalImport<typeof import('../../app/composables/use/game/wsmanagers/admin')>()
  return {
    ...actual,
    // useAdminWebsocket: vi.fn().mockReturnValue({
    //   wsObject: vi.fn(),
    //   players: ref(playersFixture),
    // })
  }
})

describe.todo('Blindtest Home Page', () => {
  it('should render the blindtest home page correctly', async () => {
    const component = await mountSuspended(BlindtestHome)

    console.log(component.html())
  })
})
