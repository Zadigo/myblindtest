import { describe, it, expect, vi, beforeEach } from 'vitest'
import { usePlayerWebsocket } from '~/composables/use/game/wsmanagers/player'
import { mountSuspended, mockNuxtImport } from '@nuxt/test-utils/runtime'
import { playersFixture } from '../../__fixtures__'

mockNuxtImport<typeof import('vue-router')['useRouter']>('useRouter', original => vi.fn(original))

mockNuxtImport<typeof import('vue-router')['useRoute']>('useRoute', original => vi.fn(original))

vi.mock('primevue/usetoast', async (originalImport) => {
  const actual = await originalImport<typeof import('primevue/usetoast')>()

  return {
    ...actual,
    useToast: vi.fn(() => ({
      add: vi.fn()
    }))
  }
})

const { mockedDocument } = vi.hoisted(() => {
  return {
    mockedDocument: vi.fn()
  }
})

vi.mock('firebase/firestore', async (originalImport) => {
  const actual = await originalImport<typeof import('firebase/firestore')>()

  return {
    ...actual,
    arrayUnion: vi.fn(),
    doc: mockedDocument,
    updateDoc: vi.fn()
  }
})

describe('Composable structure', { tags: ['composable'] }, () => {
  let mockTemplate: ReturnType<typeof mountSuspended>
  let result: ReturnType<typeof usePlayerWebsocket>
  
  beforeEach(async () => {
    const component = defineComponent({
      template: `
      <div>
        {{ isConnected }}
      </div>
      `,
      setup() {
        result = usePlayerWebsocket()
        return result
      }
    })

    mockTemplate = await mountSuspended(component)
  })

  it('should have the expected properties and methods', () => {
    const expectedProperties = [
      'wsObject',
      'isConnected',
      'blindTestDoc',
      'backgroundImage',
      'isCorrectGuess',
      'showAnswer',
      'correctSong',
      'isIncorrectGuess',
      'isReady',
      'players',
      'player',
      'selected',
      'isAnswered',
      'query'
    ]

    expectedProperties.forEach((item) => {
      expect(result).toHaveProperty(item)
    })
  })

  it('should return default values', () => {
    expect(result.selected.value).toBeNull()
    expect(result.isAnswered.value).toBe(false)
    expect(result.backgroundImage.value).toBe('/dancing1.jpg')
    expect(result.correctSong.value).toBeNull()
    expect(result.isCorrectGuess.value).toBe(false)
    expect(result.isIncorrectGuess.value).toBe(false)
    expect(result.showAnswer.value).toBe(false)
  })

  it('should be able to use websocket', async () => {
    mockedDocument.mockReturnValue({
      players: playersFixture,
    })

    // console.log(mockTemplate.html())
  })
})
