import { describe, it, expect, vi } from 'vitest'
import HomePage from '../../app/pages/index.vue'
import GeneralSettings from '../../app/components/home/GeneralSettings.vue'
import {  mountSuspended, renderSuspended } from '@nuxt/test-utils/runtime'
import type { SettingsApiResponse } from '../../app/types/index'
// import { flushPromises, mount } from '@vue/test-utils'

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

describe('Home Page', () => {
  it('should render the home page correctly', async () => {
    const component = await mountSuspended(HomePage, {
      global: {
        mocks: {
          $t: t,
        }
      }
    })

    const generalSettings = component.findComponent(GeneralSettings)
    expect(generalSettings.exists()).toBe(true)


    // const resetButton = component
  })

  it('should contain required buttons', async () => {
    const { findByText } = await renderSuspended(HomePage)

    const buttons = ['Reset', 'Start']
    buttons.forEach(item => {
      const resetBtn = findByText(item)
      expect(resetBtn).toBeDefined()
    })
  })

  // it('should toggle dark mode', async () => {
  //   const component = await mountSuspended(HomePage)
  //   const toggleEl = component.find('#dark-mode')

  //   expect(toggleEl).toBeDefined()
  //   toggleEl.trigger('click')

  //   await nextTick()

  //   expect(toggleEl.attributes('checked')).toBeDefined()
  // })
})
