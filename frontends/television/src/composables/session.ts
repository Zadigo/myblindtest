export const useSession = createGlobalState(() => {
  const sessionId = useLocalStorage<string>('tvBlindTestId', '')

  return {
    sessionId
  }
})
