import { doc } from 'firebase/firestore'
import { useDocument, useFirestore } from 'vuefire'
import type {CustomLocationQuery } from '#shared/types'
import type { CacheSession } from '#shared/types/session'
import type { SessionApiResponse } from '#shared/types/session'
import { SESSION_COOKIE_NAME } from '#shared/session_constants'


export function useCreateSession() {
  if (import.meta.client) {
    const sessionId = useSessionStorage<Nullable<string>>(SESSION_COOKIE_NAME, null)
    if (!sessionId.value) {
      callOnce('createSession', async () => {
        const response = await $fetch<SessionApiResponse>('/api/session/new', { method: 'POST' })
        sessionId.value = response.sessionId
      })
    }
  }
}

/**
 * This composable manages the blindtest session. It handles creating,
 * retrieving, updating, and deleting the session data in Firestore. A session
 * can be considered as a game instance where players can join and participate
 * in a blindtest
 */
export async function useSessionComposable() {
  const { data } = await useAsyncData('session', () => $fetch<CacheSession>('/api/session', { method: 'GET' }))

  const previousSettings = ref<CacheSession>()

  watch(data, async (newValue) => {
    console.log(newValue)
    try {
      await $fetch('/api/session/update', {
        method: 'PATCH',
        body: newValue,
        onRequest() {
          previousSettings.value = data.value
          data.value = newValue
        },
        onResponseError() {
          data.value = previousSettings.value
        },
        async onResponse() {
          await refreshNuxtData('settings')
        }
      })
    } catch (error) {
      console.error('Failed to update session:', error)
    }
  })

  async function remove() {
    $fetch('/api/session/remove', {
      method: 'DELETE'
    })
  }

  async function reset() {
    $fetch('/api/session/reset', {
      method: 'POST'
    })
  }

  const sessionId = useSessionStorage<Nullable<string>>(SESSION_COOKIE_NAME, null)

  const hasExistingSession = computed(() => !!sessionId.value)

  return {
    sessionId,
    currentSettings: data,
    remove,
    reset,
    hasExistingSession
  }
}

/**
 * This composable is used to manage the player session state
 * across the application. It takes the firebase session ID
 * directly from the current url
 * 
 */
export const usePlayerSession = createGlobalState(() => {
  const firestore = useFirestore()
  const routeQuery = useRoute().query as CustomLocationQuery

  const docRef = doc(firestore, 'blindtests', routeQuery.id || '')
  const currentSettings = useDocument<CacheSession>(docRef)

  return {
    currentSettings
  }
})
