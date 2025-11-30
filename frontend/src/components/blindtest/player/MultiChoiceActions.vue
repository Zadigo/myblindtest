<template>
  <div>
    <div class="p-5 rounded-lg ">
      <div :class="colorTheme" class="flex-col place-items-center space-y-3">
        <vue-icon icon="lucide:circle-check" class="w-10 h-10" />
        <span>Answered n°{{ playerAnswer?.answer_index }}</span>
      </div>
    </div>

    <reconnect-button :player-id="playerId" />
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ playerId: string }>()

/**
 * Answer
 */

const { currentSettings } = usePlayerSession()
const playerAnswer = computed(() => useArrayFind(currentSettings.value?.playerAnswers || [], (answer) => answer.player_id === props.playerId).value)
const answer = computed(() => useArrayFind(currentSettings.value?.availableAnswers || [], (ans) => ans.id === playerAnswer.value?.answer_index).value)

const isCorrect = computed(() => isDefined(answer) && answer.value.is_correct_answer)

const colorTheme = computed(() => {
  return {
    'bg-secondary-500 dark:bg-secondary-800': isCorrect.value,
    'bg-danger-500 dark:bg-danger-600': !isCorrect.value
  }
})
</script>
