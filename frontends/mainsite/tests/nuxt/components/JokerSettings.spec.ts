import JokerSettings from '../../../app/components/home/JokerSettings.vue'
import { describe, it, expect, vi } from 'vitest'
import { mountSuspended } from '@nuxt/test-utils/runtime'

describe('Joker Settings', () => {
  it('should render the home page correctly', async () => {
    const component = await mountSuspended(JokerSettings)
    // console.log(component.html())
  })
})
