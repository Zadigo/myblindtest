<template>
  <div ref="teamBlockEl" :style="blockStyles" class="d-flex flex-column align-items-center position-relative">
    <!-- Team Name -->
    <div class="p-3 bg-dark text-light mt-4 mb-3 rounded-3">
      <h1 class="h4 fw-bold m-0 d-flex align-items-center gap-2">
        {{ teamName }}
      </h1>
    </div>
    
    <!-- Score -->
    <div ref="scoreBoxEl" class="score p-3 rounded-3 bg-dark text-light" style="width: 200px;">
      <h2 class="fs-1 w bold m-0">
        {{ teamScore }}
      </h2>

      <p class="m-0 fw-light text-lowercase">
        Points
      </p>
    </div>

    <div class="mt-5 mb-3 d-flex justify-content-center gap-2">
      <!-- :disabled="!songsStore.gameStarted" -->
      <v-btn :flat="matchedElement!=='Title'" rounded @click="handleMatch('Title')">
        <FontAwesomeIcon icon="t" class="me-2" /> Title
      </v-btn>

      <v-btn :flat="matchedElement!=='Artist'" rounded @click="handleMatch('Artist')">
        <FontAwesomeIcon icon="a" class="me-2" /> Artist
      </v-btn>

      <v-btn :flat="matchedElement!=='Both'" rounded @click="handleMatch('Both')">
        <FontAwesomeIcon icon="a" class="me-2" /> Both
      </v-btn>
    </div>

    <!-- Actions -->
    <div class="d-flex align-items-center flex-column gap-2">
      <v-btn :disabled="!songsStore.gameStarted" size="x-large" rounded @click="handleCorrectAnswer">
        <FontAwesomeIcon icon="check" class="me-2" /> Validate
      </v-btn>

      <v-btn variant="tonal" color="dark" rounded @click="emit('team:settings', teamId)">
        <FontAwesomeIcon icon="cog" />
      </v-btn>
    </div>

    <!-- Consecutive Answers -->
    <Transition class="animate__animated" enter-to-class="animate__zoomInLeft" leave-to-class="animate__fadeOutLeft">
      <h1 v-if="hasConsecutiveAnswers" id="exceptional">
        Exceptional x {{ consecutiveAnswers }}
      </h1>
    </Transition>

    <!-- Fireworks -->
    <BaseFireworks v-show="gameStarted && hasConsecutiveAnswers" />
  </div>
</template>

<script lang="ts" setup>
import { useSongs } from '@/stores/songs';
import { whenever } from '@vueuse/core';
import { storeToRefs } from 'pinia';
import { computed, ref } from 'vue';
import type { MatchedElement } from '@/types';

import BaseFireworks from '../BaseFireworks.vue';

const emit = defineEmits({
  'next-song' (_data: (number | MatchedElement)[]) {
    return true
  },
  'team:settings' (_teamId: number) {
    return true
  }
})

const props = defineProps({
  teamId: {
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
  }
})

const songsStore = useSongs()
const { cache, correctAnswers, gameStarted } = storeToRefs(songsStore)

const teamBlockEl = ref<HTMLElement>()
const scoreBoxEl = ref<HTMLElement>()
const currentBonus = ref<number>(0)

const matchedElement = ref<MatchedElement>('Both')

const team = computed(() => {
  if (cache.value) {
    return cache.value.teams[props.teamId]
  } else {
    return null
  }
})

const teamName = computed(() => {
  if (team.value && team.value.name !== "") {
    return team.value.name
  } else {
    return `Team n°${props.teamId + 1}`
  }
})

const teamScore = computed(() => {
  if (team.value) {
    return team.value.score
  } else {
    return 0
  }
})

const blockStyles = computed(() => {
  return `margin-left:${props.marginLeft}rem;margin-right:${props.marginRight}rem;`
})

// Checks when a team has given multiple consecutive
// answers (at least 2)
const MIN_CONSECUTIVE = 2; // or whatever number you want

const consecutiveAnswers = computed(() => {
  if (correctAnswers.value.length < MIN_CONSECUTIVE) {
    return 0;
  }

  let count = 0;
  
  for (let i = correctAnswers.value.length - 1; i >= 0; i--) {
    const answer = correctAnswers.value[i];
    
    if (answer.teamId === props.teamId) {
      count++;
    } else {
      break;
    }
  }

  return count >= MIN_CONSECUTIVE ? count : 0;
});

// Flag that explicitly returns if the team has
// answered consecutive answers
const hasConsecutiveAnswers = computed(() => {
  return consecutiveAnswers.value > MIN_CONSECUTIVE
})

whenever(hasConsecutiveAnswers, () => {
  // Do something
  currentBonus.value = 0
})

async function handleAnimation () {
  if (scoreBoxEl.value) {
    const animationClasses = ['animate__animated', 'animate__heartBeat', 'animate__repeat-1'];
    
    // First remove the classes if they exist
    scoreBoxEl.value.classList.remove(...animationClasses);
    
    // Force a reflow to restart the animation
    void scoreBoxEl.value.offsetWidth;
    
    // Add the classes back
    scoreBoxEl.value.classList.add(...animationClasses);
  }
}

async function handleCorrectAnswer () {
  await handleAnimation()
  emit('next-song', [props.teamId, matchedElement.value])
  matchedElement.value = 'Both'
}

// Allows us to determine whether the user matched the
// artist and/or the song title for the current given song
function handleMatch(match: MatchedElement) {
  matchedElement.value = match
}
</script>

<style lang="scss" scoped>
h1#exceptional {
  font-family: "Rowdies", "Roboto", sans-serif;
  margin-top: 4rem;
}
</style>
