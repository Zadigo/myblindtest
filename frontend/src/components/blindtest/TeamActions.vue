<template>
  <div class="my-10 flex-col justify-center space-y-5">
    <div class="flex justify-around gap-2">
      <sound-effect id="sound-title" name="camera">
        <template #default="{ attrs }">
          <VoltContrastButton :variant="matchedElement === 'Title' ? 'filled' : 'outlined'" class="w-full" @click="attrs.playSound(() => handleMatch('Title'))">
            <vue-icon icon="lucide:star-half" />
            Title
          </VoltContrastButton>
        </template>
      </sound-effect>
      
      <sound-effect id="sound-artist" name="camera">
        <template #default="{ attrs }">
          <VoltContrastButton :variant="matchedElement === 'Artist' ? 'filled' : 'outlined'" class="w-full" @click="attrs.playSound(() => handleMatch('Artist'))">
            <vue-icon icon="lucide:star-half" />
            Artist
          </VoltContrastButton>
        </template>
      </sound-effect>
      
      <sound-effect id="sound-both" name="camera">
        <template #default="{ attrs }">
          <VoltContrastButton :variant="matchedElement === 'Both' ? 'filled' : 'outlined'" class="w-full" @click="attrs.playSound(() => handleMatch('Both'))">
            <vue-icon icon="lucide:star" />
            Both
          </VoltContrastButton>
        </template>
      </sound-effect>
    </div>
    
    <VoltContrastButton class="w-full" @click="proxySendCorrectAnswer">
      <vue-icon icon="lucide:check" />
      Validate
    </VoltContrastButton>
  </div>
</template>

<script setup lang="ts">
import type { Team, Undefineable } from '@/types';

const { sendCorrectAnswer } = useGameWebsocketIndividual()
const matchedElement = ref<MatchedPart>('Both')

const props = defineProps<{ team: Undefineable<Team> }>()
const emit = defineEmits<{ animate: [] }>()

async function proxySendCorrectAnswer() {
  if (props.team) {
    emit('animate')

    console.log('Correct answer', props.team)

    sendCorrectAnswer(props.team.id, matchedElement.value)
    matchedElement.value = 'Both'
  } else {
    console.error('handleCorrectAnswer', 'No team')
  }
}

function handleMatch(match: MatchedPart) {
  matchedElement.value = match
}
</script>
