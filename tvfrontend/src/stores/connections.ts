export const useConnectionStore = defineStore('connections', () => {
  const isConnected = ref<boolean>(false)
  const isAccepted = ref<boolean>(false)

  const toggleIsConnected = useToggle(isConnected)
  const toggleIsAccepted = useToggle(isAccepted)

  const canDiffuse = computed(() => isConnected.value && isAccepted.value)

  return {
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
