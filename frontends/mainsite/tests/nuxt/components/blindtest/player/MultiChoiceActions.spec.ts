import { describe, it, vi, expect } from 'vitest'
import MultiChoiceActions from '../../../../../app/components/blindtest/player/MultiChoiceActions.vue'
import { mountSuspended } from '@nuxt/test-utils/runtime'

vi.mock('../../../../../app/composables/use/session', async (importOriginal) => {
const actual = await importOriginal<typeof import('../../../../../app/composables/use/session')>()
  return {
    ...actual
  }
})

describe('MultiChoiceActions', () => {
  it('should render the multi choice actions correctly', async () => {
    const component = await mountSuspended(MultiChoiceActions)

    // console.log(component.html())
  })
})
