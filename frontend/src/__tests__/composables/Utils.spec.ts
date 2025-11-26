import { describe, it, expect, vi } from 'vitest'
import type { SettingsApiResponse } from '../../types'
import { useLoadAutocompleteData } from '../../composables'

vi.mock('@vueuse/core', async (importActual) => {
  const actual = await importActual<typeof import('@vueuse/core')>()
  return {
    ...actual,
    useMemoize: () => {
      return {
        load: () => Promise.resolve({
          period: { minimum: 10, maximum: 90 },
          count_by_genre: [
            { genre: 'Rock', count: 50 },
            { genre: 'Pop', count: 30 },
            { genre: 'Jazz', count: 20 }
          ]
        } as SettingsApiResponse)
      }
    }
  }
})

describe('useLoadAutocompleteData', () => {
  it('should load autocomplete data from API', async () => {
    const { autocomplete, minimumPeriod, maximumPeriod, genres } = useLoadAutocompleteData(false)

    expect(autocomplete.value).toBeDefined()
    expect(await minimumPeriod.value).toBe(10)
    // expect(await maximumPeriod.value).toBe(90)
    // expect(await genres.value).toEqual([
    //   { label: 'Rock', name: 'Rock' },
    //   { label: 'Pop', name: 'Pop' },
    //   { label: 'Jazz', name: 'Jazz' }
    // ])
  })
})
