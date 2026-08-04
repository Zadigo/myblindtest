import { describe, it, expect, vi } from 'vitest'
import CreateSongs from '../../app/pages/create-songs.vue'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import type { SettingsApiResponse } from '../../app/types/index.ts'

const t = vi.fn((key: string) => key)

vi.mock('i18n', () => ({
  useI18n: () => ({
    t,
    locale: ref('fr'),
  })
}))

vi.mock('../../app/composables/use/utils', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../../app/composables/use/utils.ts')>()
  return {
    ...actual,
    useLoadAutocompleteData: vi.fn().mockReturnValue({
      genres: ref<{ label: string, name: string }[]>([]),
      autocomplete: ref<SettingsApiResponse | undefined>(undefined),
    })
  }
})

describe('Create Songs Page', () => {
  it('should render the create songs page correctly', async () => {
    const component = await mountSuspended(CreateSongs, {
      global: {
        mocks: {
          $t: t,
        }
      }
    })

    // console.log(component.html())

    const titleEl = component.find('h1')
    expect(titleEl.exists()).toBe(true)
    expect(titleEl.text()).toBe('Create songs')
  })
})
