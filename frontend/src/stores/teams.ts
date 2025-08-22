import { useSessionStore } from './session'

export const useTeamsStore = defineStore('teams', () => {
  const sessionStore = useSessionStore()
  const { currentSettings } = storeToRefs(sessionStore)

  const teams = computed(() => currentSettings.value.cache.teams)
  const teamOne = computed(() => teams.value[0])
  const teamTwo = computed(() => teams.value[1])

  return {
    teams,
    teamOne,
    teamTwo
  }
})
