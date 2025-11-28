<template>
  <volt-card>
    <template #content>
      <div id="multiple-choice-answers">
        <volt-fluid class="space-y-3">
          <volt-secondary-button v-for="(item, idx) in currentSettings?.availableAnswers" :key="item.id" :disabled="isAnswered" size="large" class="flex justify-start" rounded @click="() => selectAnswer(idx)">
            <vue-icon v-if="isAnswered && selected === idx" icon="lucide:check" class="font-bold" />
            <span class="font-bold">{{ item.name }}</span> - {{ item.artist__name }}
          </volt-secondary-button>
        </volt-fluid>
      </div>
    </template>
  </volt-card>
</template>

<script setup lang="ts">
const { wsObject } = usePlayerWebsocket()
const { stringify } = useWebsocketMessage()
const { currentSettings } = usePlayerSession()

const selected = ref<number | null>(null)
const isAnswered = ref(false)

function selectAnswer(id: number) {
  isAnswered.value = true
  selected.value = id
  wsObject.send(stringify({ action: 'submit_answer', answer_index: id }))
}
</script>
