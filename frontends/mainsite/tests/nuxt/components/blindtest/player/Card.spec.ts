import { describe, it } from 'vitest'
import Card from '../../../../../app/components/blindtest/player/Card.vue'
import { mountSuspended } from '@nuxt/test-utils/runtime'

describe('Card', () => {
  it('should render the card correctly', async () => {
    const component = await mountSuspended(Card)

    // console.log(component.html())
  })
})
