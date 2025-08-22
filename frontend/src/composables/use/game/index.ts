import type { RandomizerData } from '@/components/randomizer'
import type { Ref } from 'vue'
import type { WebsocketRandomizeGenre } from '@/types'

export { useGameWebsocket, useWebsocketMessage } from './ws_manager'

export * from './ws_manager'

/**
 * Composable that triggers and runs the
 * wheel randomizer
 */
export function useWheelRandomizer(ws: Ref<WebSocket>) {
  const showWheel = ref<boolean>(false)
  const randomizerEl = ref<HTMLElement>()

  const { send } = useWebsocketMessage()

  /**
   * Function that gets called once the
   * spinning has finished
   *
   * @param value The genre to get
   */
  function randomizerComplete(value: string | undefined | RandomizerData) {
    if (value) {
      setTimeout(() => {
        showWheel.value = false

        const result = send<WebsocketRandomizeGenre>({
          action: 'randomize_genre',
          temporary_genre: value
        })

        if (result) {
          ws.value.send(result)
        }
      }, 3000)
    }
  }

  return {
    showWheel,
    randomizerEl,
    randomizerComplete
  }
}

export function useGameAnswering() {
  return {
    
  }
}
