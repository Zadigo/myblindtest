<template>
  <div id="left" ref="teamBlockEl" class="p-5 h-screen">
    <div id="team" :class="blockPosition" class="flex-col w-7/12">
      <volt-card class="w-full text-center border-none">
        <template #content>
          <h1 ref="scoreBoxEl" class="text-5xl font-bold">
            {{ teamScore }}
          </h1>

          <p class="font-light uppercase">
            Points ({{ teamName }})
          </p>
        </template>
      </volt-card>

      <!-- Actions -->
      <volt-card class="mt-2 mb-10 border-none">
        <template #content>
          <div class="flex justify-center gap-2">
            <volt-button :variant="matchedElement === 'Title' ? '' : 'outlined'" size="small" @click="handleMatch('Title')">
              <vue-icon icon="fa-solid:star-half" />
              Title
            </volt-button>

            <volt-button :variant="matchedElement === 'Artist' ? '' : 'outlined'" size="small" @click="handleMatch('Artist')">
              <vue-icon icon="fa-solid:star-half" />
              Artist
            </volt-button>

            <volt-button :variant="matchedElement === 'Both' ? '' : 'outlined'" size="small" @click="handleMatch('Both')">
              <vue-icon icon="fa-solid:star" />
              Both
            </volt-button>
          </div>

          <div class="flex justify-center mt-4 w-full">
            <volt-button :disabled="!gameStarted" class="w-10/13 self-center" variant="default" @click="handleCorrectAnswer">
              <vue-icon icon="fa-solid:check" />
              Validate
            </volt-button>
          </div>
        </template>
      </volt-card>

      <div class="flex gap-1 justify-center p-5 mt-3">
        <div v-for="i in 5" :key="i" class="p-2 bg-brand-shade-5/50 rounded-md w-1/6" />
      </div>

      <!-- Consecutive Answers -->
      <Transition class="animate__animated" enter-to-class="animate__zoomInLeft" leave-to-class="animate__fadeOutLeft">
        <h1 v-if="hasConsecutiveAnswers" class="text-5xl font-bold text-gray-700">
          Exceptionnel x {{ consecutiveAnswers }}
        </h1>
      </Transition>

      <!-- Fireworks -->
      <base-fireworks v-show="gameStarted && hasConsecutiveAnswers" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { MatchedPart } from '@/data'

const emit = defineEmits<{ 'next-song': [data: [ teamId: string, match: MatchedPart]] }>()

const { teamIndex = 1, marginRight = 0, marginLeft = 0, diffusionMode = false, blockPosition = 'me-auto' } = defineProps<{ 
  teamIndex: number, 
  marginRight?: number, 
  marginLeft?: number, 
  diffusionMode?: boolean, 
  blockPosition?: string 
}>()

const songsStore = useSongs()
const { correctAnswers, gameStarted } = storeToRefs(songsStore)

const teamBlockEl = useTemplateRef<HTMLElement>('teamBlockEl')
const scoreBoxEl = useTemplateRef<HTMLElement>('scoreBoxEl')

const currentBonus = ref<number>(0)
const matchedElement = ref<MatchedPart>('Both')

const teamStore = useTeamsStore()
const { teams } = storeToRefs(teamStore)

const team = teamStore.getTeamByIndex(teamIndex)

const teamName = computed(() => {
  if (team.value) {
    return team.value.name === '' ? team.value.id : team.value.name
  } else {
    return 'Team XYZ'
  }
})

const teamScore = computed(() => team.value ? team.value.score : 0)

// Checks when a team has given multiple consecutive
// answers (at least 2)
const MIN_CONSECUTIVE = 2

const consecutiveAnswers = computed(() => {
  if (correctAnswers.value.length < MIN_CONSECUTIVE) {
    return 0
  }

  let count = 0

  for (let i = correctAnswers.value.length - 1; i >= 0; i--) {
    const answer = correctAnswers.value[i]

    if (answer && (answer.teamId === (team.value && team.value.id))) {
      count++
    } else {
      break
    }
  }

  return count >= MIN_CONSECUTIVE ? count : 0
})

/**
 * Flag that explicitly returns if the team has
 * answered consecutive answers
 */
const hasConsecutiveAnswers = computed(() => consecutiveAnswers.value > MIN_CONSECUTIVE)

whenever(hasConsecutiveAnswers, () => {
  // Do something
  currentBonus.value = 0
})

/**
 * Handles the different animations on the page
 */
async function handleAnimation() {
  if (scoreBoxEl.value) {
    const animationClasses = ['animate__animated', 'animate__heartBeat', 'animate__repeat-1']

    // First remove the classes if they exist
    scoreBoxEl.value.classList.remove(...animationClasses)

    // Force a reflow to restart the animation
    void scoreBoxEl.value.offsetWidth

    // Add the classes back
    scoreBoxEl.value.classList.add(...animationClasses)
  }
}

/**
 * Function that handles the correct
 * answser from a given team
 */
async function handleCorrectAnswer() {
  if (team.value) {
    await handleAnimation()
    
    console.log('Correct answer', team.value)

    emit('next-song', [team.value.id, matchedElement.value])
    matchedElement.value = 'Both'
  } else {
    console.error('handleCorrectAnswer', 'No team')
  }
}

/**
 * Allows us to determine whether the user matched the
 * artist and/or the song title for the current given song
 *
 * @param match The matched element
 */
function handleMatch(match: MatchedPart) {
  matchedElement.value = match
}
</script>
