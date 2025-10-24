/**
 * Devices Store
 * Used to manage devices within the blindtest session
 */
export const useDevicesStore = defineStore('devices', () => {
  const showDevicesModal = ref<boolean>(false)
  const devices = reactive({ smartphones: [], televisions: [] })


  function add(device: 'smartphone' | 'television', data) {
    switch (device) {
      case 'smartphone':
        devices.smartphones.push(data)
        break

      case 'television':
        devices.televisions.push(data)
        break
    
      default:
        break
    }
  }

  function remove(device: 'smartphone' | 'television', id: string) {
    const item = useArrayFind(devices[device], item => item.id === id)

    if (isDefined(item)) item.active = false
  }

  return {
    showDevicesModal,
    devices,
    add,
    remove
  }
})
