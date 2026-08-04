import { describe, it, expect, vi } from 'vitest'
import TeamBlock from '../../../app/components/blindtest/TeamBlock.vue'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { cachedSession } from '../../__fixtures__'

// This component might be deprecrated
describe.todo('TeamBlock', () => {
  it('should render the team block correctly', async () => {
    const component = await mountSuspended(TeamBlock)

    // console.log(component.html())
  })
})
