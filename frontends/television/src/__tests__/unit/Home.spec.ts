import HomePage from '../../pages/HomePage.vue'
import { describe, it, expect, vi } from 'vitest'
import { shallowMount } from '@vue/test-utils'

vi.stubGlobal('useConnectionStore', () => ({
  code: ref(''),
  isConnected: ref(false),
}))

vi.stubGlobal('useGameWebsocket', () => ({
  connect: vi.fn(),
  disconnect: vi.fn(),
  sendMessage: vi.fn()
}))

vi.stubGlobal('useRouter', () => ({
  push: vi.fn()
}))

describe('HomePage', () => {
  it('should render the HomePage component', () => {
    const wrapper = shallowMount(HomePage)
    expect(wrapper.exists()).toBe(true)

    const titleEl = wrapper.find('h1')
    expect(titleEl.exists()).toBe(true)

    // const inputEl = wrapper.find('input')
    // expect(inputEl.exists()).toBe(true)
    // console.log(wrapper.html())
  })
})
