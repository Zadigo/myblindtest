<template>
  <div id="left" ref="teamBlockEl" class="p-5 h-screen">
    <div id="team" :class="blockPosition" class="flex-col w-7/12">
      <Card class="w-full text-center border-none">
        <CardContent>
          <h1 ref="scoreBoxEl" class="text-5xl font-bold">
            {{ teamScore }}
          </h1>

          <p class="font-light uppercase">
            Points ({{ teamName }})
          </p>
        </CardContent>
      </Card>

      <!-- Actions -->
      <Card class="mt-2 mb-10 border-none">
        <CardContent>
          <div class="flex justify-center gap-2">
            <Button :variant="matchedElement === 'Title' ? 'default' : 'secondary'" @click="handleMatch('Title')">
              <VueIcon name="fa-solid:t" />
              Title
            </Button>

            <Button :variant="matchedElement === 'Artist' ? 'default' : 'secondary'" @click="handleMatch('Artist')">
              <VueIcon name="fa-solid:a" />
              Artist
            </Button>

            <Button :variant="matchedElement === 'Both' ? 'default' : 'secondary'" @click="handleMatch('Both')">
              <VueIcon name="fa-solid:t" />
              Both
            </Button>
          </div>

          <div class="flex justify-center mt-4 w-full">
            <Button :disabled="!gameStarted" class="w-10/13 self-center" variant="default" @click="handleCorrectAnswer">
              <VueIcon icon="fa-solid:check" />
              Validate
            </Button>
          </div>
        </CardContent>
      </Card>

      <div class="flex gap-1 justify-center p-5 mt-3">
        <div v-for="i in 5" :key="i" class="p-2 bg-yellow-100 rounded-md w-1/6" />
      </div>

      <!-- Consecutive Answers -->
      <Transition class="animate__animated" enter-to-class="animate__zoomInLeft" leave-to-class="animate__fadeOutLeft">
        <h1 v-if="hasConsecutiveAnswers" class="text-5xl font-bold text-gray-700">
          Exceptionnel x {{ consecutiveAnswers }}
        </h1>
      </Transition>

      <!-- Fireworks -->
      <BaseFireworks v-show="gameStarted && hasConsecutiveAnswers" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useSongs } from '@/stores/songs'
import { whenever } from '@vueuse/core'
import { storeToRefs } from 'pinia'
import { computed, ref } from 'vue'
import type { MatchedElement } from '@/types'

import BaseFireworks from '../BaseFireworks.vue'

const emit = defineEmits({
  'next-song'(_data: (number | MatchedElement)[]) {
    return true
  }
})

const props = defineProps({
  teamIndex: {
    type: Number,
    default: 1
  },
  marginRight: {
    type: Number,
    default: 0
  },
  marginLeft: {
    type: Number,
    default: 0
  },
  diffusionMode: {
    type: Boolean,
    default: false
  },
  blockPosition: {
    type: String,
    default: 'me-auto'
  }
})

const songsStore = useSongs()
const { cache, correctAnswers, gameStarted } = storeToRefs(songsStore)

const teamBlockEl = ref<HTMLElement>()
const scoreBoxEl = ref<HTMLElement>()
const currentBonus = ref<number>(0)

const matchedElement = ref<MatchedElement>('Both')

const team = computed(() => {
  return cache.value.teams[props.teamIndex]
})

const teamName = computed(() => {
  if (team.value) {
    if (team.value.name !== '') {
      return team.value.name
    } else {
      return team.value.id
    }
  } else {
    return 'Team'
  }
})

const teamScore = computed(() => {
  if (team.value) {
    return team.value.score
  } else {
    return 0
  }
})

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

    if (answer.teamId === team.value.id) {
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
const hasConsecutiveAnswers = computed(() => {
  return consecutiveAnswers.value > MIN_CONSECUTIVE
})

whenever(hasConsecutiveAnswers, () => {
  // Do something
  currentBonus.value = 0
})

/**
 *
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
 *
 */
async function handleCorrectAnswer() {
  if (team.value) {
    await handleAnimation()
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
function handleMatch(match: MatchedElement) {
  matchedElement.value = match
}
</script>
