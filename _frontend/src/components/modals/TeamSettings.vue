<template>
  <v-dialog v-model="show" persistent style="width:500px;">
    <v-card>
      <v-card-item>
        <v-btn variant="text" @click="show=false">
          <FontAwesomeIcon icon="close" />
        </v-btn>
      </v-card-item>

      <v-card-text>
        <v-text-field v-model="teamName" placeholder="Team name" variant="solo-filled" flat />

        <div class="d-flex justify-content-center mb-4">
          <VueColorWheel v-model:color="wheelColor" wheel="aurora" harmony="monochromatic" :radius="160" :default-color="wheelColor" @change="handleChangeColors" />
        </div>

        <v-text-field v-model="wheelColor" variant="solo-filled" flat />
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="ts" setup>
import { useDebounce } from '@vueuse/core'
import { useSongs } from '@/stores/songs'
import { computed, ref, watch } from 'vue'

import type { Harmony } from 'vue-color-wheel'
import { VueColorWheel } from 'vue-color-wheel'

const songsStore = useSongs()

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  teamId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits({
  'update:modelValue'(_value: boolean) {
    return true
  }
})

const wheelColor = useDebounce(ref('#40ffff'))
const colorList = ref<Harmony[]>()

const teamIndex = computed(() => {
  return songsStore.cache.teams.findIndex(x => x.id === props.teamId)
})

watch(wheelColor, (newValue) => {
  songsStore.cache.teams[teamIndex.value].color = newValue
})

const team = computed(() => {
  return songsStore.cache.teams.find(x => x.id === props.teamId)
})

const teamName = computed({
  get: () => team.value?.name || 'Team',
  set: (value) => {
    if (team.value) {
      team.value.name = value
    }
  }
})

const show = computed({
  get: () => props.modelValue,
  set: (value) => {
    emit('update:modelValue', value)
  }
})

function handleChangeColors(harmonyColors: Harmony[]) {
  colorList.value = harmonyColors
}
</script>
