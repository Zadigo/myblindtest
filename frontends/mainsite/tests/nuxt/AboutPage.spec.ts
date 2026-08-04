import { describe, it, expect, vi } from 'vitest'
import AboutPage from '../../app/pages/about.vue'
import { mountSuspended } from '@nuxt/test-utils/runtime'

describe('About Page', () => {
  it('should render the about page correctly', async () => {
    const component = await mountSuspended(AboutPage)
    // console.log(component.html())
    
    const titleEl = component.find('h1')
    expect(titleEl.exists()).toBe(true)
  })
})
