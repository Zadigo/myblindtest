import TopActionsBar from '../../../../../app/components/blindtest/score/TopActionBar.vue'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import { describe, it, expect } from 'vitest'

describe('TopActionsBar', () => {
  it('should render the top actions bar correctly', async () => {
    const component = await mountSuspended(TopActionsBar)

    const buttonEl = component.find('button')
    expect(buttonEl.exists()).toBe(true)
    expect(buttonEl.attributes('disabled')).toBeUndefined()
  })

  it('should emit toggle-graph event when the button is clicked', async () => {
    const component = await mountSuspended(TopActionsBar)

    const buttonEl = component.find('button')
    await buttonEl.trigger('click')

    expect(component.emitted()).toHaveProperty('toggle-graph')
  })
})
