import type { RandomizerData } from "@/components/randomizer"

/**
 * Composable that triggers and runs the
 * wheel randomizer
 */
export const useWheelRandomizer = createGlobalState((ws?: ReturnType<typeof useGameWebsocket>['wsObject'], autoClose = false) => {
  const showWheel = ref<boolean>(false)
  const randomizerEl = useTemplateRef('randomizerEl')

  const { stringify } = useWebsocketMessage()

  function randomizerComplete(value: string | undefined | RandomizerData) {
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
     *
     * @param value The genre to get
     */
    randomizerComplete
  }
})
