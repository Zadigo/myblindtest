<template>
  <volt-card>
    <template #content>
      <div id="multiple-choice-answers">
        <volt-fluid class="space-y-3">
          <volt-secondary-button v-for="(item, idx) in currentSettings?.availableAnswers" :key="item.id" :disabled="isAnswered" size="large" class="flex justify-start z-30" rounded @click="() => selectAnswer(idx)">
            <vue-icon v-if="isAnswered && selected === idx" icon="lucide:check" class="font-bold" />
            <span class="font-bold">{{ item.name }}</span> - {{ item.artist__name }}
          </volt-secondary-button>
        </volt-fluid>
      </div>
    </template>
  </volt-card>
</template>

<script setup lang="ts">
const { currentSettings } = usePlayerSession()

const { wsObject, isAnswered, selected } = usePlayerWebsocket()
const { stringify } = useWebsocketMessage()

function selectAnswer(id: number) {
  selected.value = id
  wsObject.send(stringify({ action: 'submit_answer', answer_index: id }))
}
</script>
