import { describe, it, expect, vi } from 'vitest'
import HomePage from '../../app/pages/index.vue'
import GeneralSettings from '../../app/components/home/GeneralSettings.vue'
import {  mountSuspended } from '@nuxt/test-utils/runtime'
import type { SettingsApiResponse } from '../../app/types'

const t = vi.fn((key: string) => key)

vi.mock('i18n', () => ({
  useI18n: () => ({
    t,
    locale: ref('fr'),
  })
}))

vi.mock('../../app/composables/use/utils', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../../app/composables/use/utils')>()
  return {
    ...actual,
    useLoadAutocompleteData: vi.fn().mockReturnValue({
      genres: ref<{ label: string, name: string }[]>([]),
      autocomplete: ref<SettingsApiResponse | undefined>(undefined),
    })
  }
})

describe('Home Page', () => {
  it('should render the home page correctly', async () => {
    const component = await mountSuspended(HomePage, {
      global: {
        mocks: {
          $t: t,
        }
      }
    })
    // console.log(component.html())

    const generalSettings = component.findComponent(GeneralSettings)
    expect(generalSettings.exists()).toBe(true)
  })
})
