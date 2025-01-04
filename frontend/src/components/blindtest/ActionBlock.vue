<template>
  <div :id="`team${teamId}`" :style="`width:100%;background-color:${elementColor};`" class="rounded-2 p-3 text-center">
    <p class="fw-bold">
      {{ teamName }}
    </p>

    <div class="d-flex justify-content-center gap-2">      
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
import { toast } from 'vue-sonner';

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
  if (team.value && team.value.name !== "") {
    return team.value.name
  } else {
    return `Team n°${props.teamId}`
  }
})

const elementColor = computed(() => {
  if (team.value && team.value.color) {
    return team.value.color
  } else {
    return 'rgba(33,150,243, 1)'
  }
})

// Adds a value to the current
// team's score
function handleScore () {
  if (team.value) {
    team.value.score += cache.value.settings.pointValue
  } else {
    toast.error('No team was present or cache is empty')
  }
}

function handleAnswer () {
  handleScore()
  emit('next-song', props.teamId)
}
</script>
