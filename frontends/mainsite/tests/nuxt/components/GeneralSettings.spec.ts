import GeneralSettings from '../../../app/components/home/GeneralSettings.vue'
import { describe, it, expect, vi } from 'vitest'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import type { SettingsApiResponse } from '~/types'
import { cachedSession } from '../../__fixtures__'

vi.mock('../../../app/composables/use/utils', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../../../app/composables/use/utils')>()
  return {
    ...actual,
    useLoadAutocompleteData: vi.fn().mockReturnValue({
      genres: ref<{ label: string, name: string }[]>([]),
      autocomplete: ref<SettingsApiResponse | undefined>(undefined),
    })
  }
})

vi.mock('../../../app/composables/use/session', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../../../app/composables/use/session')>()
  return {
    ...actual,
    useSession: vi.fn(() => {
      return {
        currentSettings: cachedSession
      }
    })
  }
})

describe('General Settings', () => {
  it('should render the home page correctly', async () => {
    const component = await mountSuspended(GeneralSettings)
    // console.log(component.html())
  })
})
