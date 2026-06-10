export const useBuzzerStore = defineStore('buzzer', () => {
  const { inc, count} = useCounter(0)

  return {
    buzzCounter: count,
    increment: inc
  }
})
