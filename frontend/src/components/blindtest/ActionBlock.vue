<template>
  <div :id="`team${teamId}`" :style="`width:100%;background-color:${elementColor};`" class="rounded-2 p-3 text-center">
    <p class="fw-bold">
      {{ teamName }}
    </p>

    <div class="d-flex justify-content-center gap-2">
      <!-- <button :disabled="!isStarted" type="button" class="btn btn-dark btn-rounded shadow-none" @click="handleNextSong(false)">
        <FontAwesomeIcon icon="xmark" />
      </button> -->
      
      <button :disabled="!isStarted" type="button" class="btn btn-dark btn-rounded shadow-none" @click="handleAnswer">
        <FontAwesomeIcon icon="check" />
      </button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useSongs } from '@/stores/songs';
import { storeToRefs } from 'pinia';
import { computed } from 'vue';

const emit = defineEmits({
  'next-song' (_data: number) {
    return true
  }
})

const props = defineProps({
  teamId: {
    type: Number,
    default: 1
  }
})

const songsStore = useSongs()
const { cache, isStarted } = storeToRefs(songsStore)

const teamIndex = computed(() => {
  const result = props.teamId - 1
  
  if (result <= 0) {
    return 0
  } else {
    return result
  }
})

const team = computed(() => {
  if (cache.value) {
    return cache.value.teams[teamIndex.value]
  } else {
    return null
  }
})

const teamName = computed(() => {
  if (cache.value) {
    // const team = cache.value.teams[teamIndex.value]

    if (team.value && team.value.name !== "") {
      return team.value.name
    }
  }
  return `Team n°${props.teamId}`
})

const elementColor = computed(() => {
  if (cache.value) {
    if (team.value) {
      return team.value.color
    }
  }
  return 'rgba(33,150,243, 1)'
})

function handleScore () {
  cache.value.teams[teamIndex.value].score += 1
}

function handleAnswer () {
  handleScore()
  emit('next-song', props.teamId)
}
</script>
