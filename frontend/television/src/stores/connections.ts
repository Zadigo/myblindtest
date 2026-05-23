import type { Song } from '@/types'

export const useConnectionStore = defineStore('connections', () => {
  const code = ref<string>('')

  const isConnected = ref<boolean>(false)
  const isAccepted = ref<boolean>(false)

  const toggleIsConnected = useToggle(isConnected)
  const toggleIsAccepted = useToggle(isAccepted)

  const canDiffuse = computed(() => isConnected.value && isAccepted.value)

  const showAnswer = refAutoReset(false, 5000)
  const answer = refAutoReset<Song | null>(null, 5000)

  return {
    answer,
    showAnswer,
    /**
     * The Firebase code to use for the blindtest
     */
    code,
    /**
     * Device is connected to the websocket
     */
    isConnected,
    /**
     * The code challenge was successful
    */
   isAccepted,
    /**
     * The device is connected and accepted
     * in the blind test
    */
   canDiffuse,
   toggleIsConnected,
   toggleIsAccepted
  }
})
