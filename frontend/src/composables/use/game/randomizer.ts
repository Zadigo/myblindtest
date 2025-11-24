import type { RandomizerData } from '@/components/blindtest/randomizer'
import type { Undefineable } from '@/types'

export const wheelDefaults: RandomizerData[] = [
  { id: 1, value: 'Pop', bgColor: '#f87171', color: '#ffffff' },
  { id: 2, value: 'Rock', bgColor: '#60a5fa', color: '#ffffff' },
  { id: 3, value: 'Hip-Hop', bgColor: '#34d399', color: '#ffffff' },
  { id: 4, value: 'Jazz', bgColor: '#fbbf24', color: '#ffffff' },
  { id: 5, value: 'Classical', bgColor: '#a78bfa', color: '#ffffff' },
  { id: 6, value: 'Electronic', bgColor: '#f472b6', color: '#ffffff' },
  { id: 7, value: 'Metal', bgColor: '#9ca3af', color: '#ffffff' },
  { id: 8, value: 'Funk', bgColor: '#10b981', color: '#ffffff' },
  { id: 9, value: 'Reggae', bgColor: '#22d3ee', color: '#ffffff' }
]

/**
 * Composable that triggers and runs the wheel randomizer. The wheel randomizer can
 * be defined as a spinning wheel that randomly selects a genre from a list of genres.
 * @param ws The websocket object to send the selected genre to the server
 * @param autoClose Whether to automatically close the wheel after selection
 */
export const useWheelRandomizer = createGlobalState((ws?: ReturnType<typeof useAdminWebsocket>['wsObject'], autoClose = false) => {
  const showWheel = ref<boolean>(false)
  const randomizerEl = useTemplateRef<HTMLElement>('randomizerEl')

  const { stringify } = useWebsocketMessage()

  function onComplete(value: Undefineable<string> | RandomizerData) {
    if (value) {
      const { start } = useTimeoutFn(() => {
        if (autoClose) showWheel.value = false

        const result = stringify({ action: 'randomize_genre', temporary_genre: value })
        if (result && isDefined(ws)) ws.send(result)
      }, 3000)

      start()
    }
  }

  return {
    /**
     * Whether to show the wheel
     * @default false
     */
    showWheel,
    /**
     * Reference to the randomizer element
     */
    randomizerEl,
    /**
     * Function that gets called once the
     * spinning has finished
     * @param value The genre to get
     */
    onComplete
  }
})
