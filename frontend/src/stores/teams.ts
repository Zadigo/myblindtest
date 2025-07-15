import type { CacheSession } from '@/types'

export const useTeamsStore = defineStore('teams', () => {
  const teams = ref<CacheSession['teams']>([])
  const teamOne = computed(() => teams.value[0])
  const teamTwo = computed(() => teams.value[1])

  return {
    teams,
    teamOne,
    teamTwo
  }
})
