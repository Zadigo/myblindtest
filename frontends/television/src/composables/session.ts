/**
 * A composable that provides access to the session ID stored in local storage.
 * This composable uses the `useLocalStorage` hook to retrieve and store the session ID, 
 * allowing components to easily access and update the session ID as needed.
 */
export const useSession = createGlobalState(() => {
  const sessionId = useLocalStorage<string>('tvBlindTestId', '')

  return {
    /**
     * The session ID stored in local storage. This value 
     * can be read and updated by components that use this composable.
     */
    sessionId
  }
})
