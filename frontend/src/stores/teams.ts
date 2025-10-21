/**
 * Store used to manage teams within the blindtest session
 */
export const useTeamsStore = defineStore('teams', () => {
  const { currentSettings } = useGlobalSessionState()

  const teams = computed(() =>  currentSettings && isDefined(currentSettings) ? currentSettings.value.teams : [])
  const teamOne = computed(() => teams.value.at(0))
  const teamTwo = computed(() => teams.value.at(1))

  function _getTeamById(id: string) {
    return teams.value.find(team => team.id === id)
  }

  const getTeamById = reactify(_getTeamById)

  function _getTeamByIndex(index: number) {
    return teams.value.at(index)
  }

  const getTeamByIndex = reactify(_getTeamByIndex)

  const firstTeamScore = computed(() => teamOne.value ? teamOne.value.score : 0)
  const secondTeamScore = computed(() => teamTwo.value ? teamTwo.value.score : 0)

  return {
    teams,
    teamOne,
    teamTwo,
    firstTeamScore,
    secondTeamScore,
    getTeamByIndex,
    getTeamById
  }
})
