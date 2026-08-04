import PointValues from '../../../../app/components/home/PointValues.vue'
import { describe, it, expect, vi } from 'vitest'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import type { SettingsApiResponse } from '~/types'
import { cachedSession } from '../../../__fixtures__/index.ts'

vi.mock('../../../app/composables/use/utils', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../../../../app/composables/use/utils.ts')>()
  return {
    ...actual,
    useLoadAutocompleteData: vi.fn().mockReturnValue({
      genres: ref<{ label: string, name: string }[]>([]),
      autocomplete: ref<SettingsApiResponse | undefined>(undefined),
    })
  }
})

vi.mock('../../../app/composables/use/session', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../../../../app/composables/use/session.ts')>()
  return {
    ...actual,
    useSession: vi.fn(() => {
      return {
        currentSettings: cachedSession
      }
    })
  }
})

describe('Point Values', () => {
  it('should render the home page correctly', async () => {
    const component = await mountSuspended(PointValues)
    // console.log(component.html())
  })
})
