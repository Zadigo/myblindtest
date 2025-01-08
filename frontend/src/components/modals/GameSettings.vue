<template>
  <v-dialog v-model="show" width="500">
    <v-card>
      <v-card-item>
        <v-btn variant="text" @click="show=false">
          <FontAwesomeIcon icon="close" />
        </v-btn>
      </v-card-item>

      <v-card-text>
        <div v-if="songsStore.cache" class="card-body">
          <label for="" class="fw-bold">Point value</label>
          <v-text-field v-model.number="songsStore.cache.settings.pointValue" type="number" min="1" variant="solo-filled" placeholder="Point value" flat />
          <v-switch v-model="songsStore.cache.settings.matchSongDifficulty" label="Match score to song difficulty" />
        </div>

        <v-divider />

        <div v-if="songsStore.cache" class="card-body">
          <label for="" class="fw-bold">Game difficulty</label>
          <v-select v-model="songsStore.cache.settings.difficultyLevel" :items="difficultyLevels" variant="solo-filled" placeholder="Blind test difficulty" flat />
          
          <label for="" class="fw-bold">Song type</label>
          <v-select v-model="songsStore.cache.settings.songType" :items="songTypes" variant="solo-filled" placeholder="Blind test difficulty" flat />
        </div>

        <v-switch label="Use bonus multiplicators" />
        <v-switch label="Save game progression" />
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { difficultyLevels, songTypes } from '@/data/defaults';
import { useSongs } from '@/stores/songs';
import { computed } from 'vue';

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const songsStore = useSongs()

const show = computed({
  get: () => props.modelValue,
  set: (value) => {
    emit('update:modelValue', value)
  }
})
</script>
