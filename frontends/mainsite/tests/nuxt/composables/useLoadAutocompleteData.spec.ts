import { mockNuxtImport, mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect, vi, beforeEach  } from 'vitest'
import type { SettingsApiResponse } from '~/types'
import { mount } from '@vue/test-utils' 

// const mockedFetch = vi.fn(async () => {
//   const response: SettingsApiResponse = {
//     count_by_genre: [
//       {
//         count: 5,
//         genre: 'Pop'
//       },
//       {
//         count: 2,
//         genre: 'Rap'
//       }
//     ],
//     period: {
//       minimum: 1,
//       maximum: 5
//     }
//   }
//   return response
// })

// vi.stubGlobal('$fetch', mockedFetch)

mockNuxtImport('$fetch', () => {
  return vi.fn(async () => {
    const response: SettingsApiResponse = {
      count_by_genre: [
        {
          count: 5,
          genre: 'Pop'
        },
        {
          count: 2,
          genre: 'Rap'
        }
      ],
      period: {
        minimum: 1,
        maximum: 5
      }
    }
    return response
  })
})

describe('useLoadAutocompleteData', () => {
  let mockTemplate: ReturnType<typeof mount>
  let composable: ReturnType<typeof useLoadAutocompleteData>

  beforeEach(async () => {
    const template = defineComponent({
      template: `
      <div>        
        <div v-for="genre in genres" :key="genre.label" :id="genre.label">
          {{ genre.label }}
        </div>
      </div>
      `,
      setup() {
        composable = useLoadAutocompleteData()
        return composable
      }
    })

    mockTemplate = mount(template)
  })

  it('sohuld initialize with default values', () => {
    expect(toValue(composable.minimumPeriod)).toEqual(1)
    expect(toValue(composable.maximumPeriod)).toEqual(5)
    expect(toValue(composable.genreDistribution)).toEqual([
      {
        count: 5,
        genre: 'Pop'
      },
      {
        count: 2,
        genre: 'Rap'
      }
    ])
    expect(toValue(composable.genreNames)).toEqual(['Pop', 'Rap'])
    expect(toValue(composable.genres)).toEqual([
      {
        label: 'Pop',
        name: 'Pop'
      },
      {
        label: 'Rap',
        name: 'Rap'
      }
    ])

    const divEl = mockTemplate.find('div#Pop')
    expect(divEl).toBeDefined()
  })
})
