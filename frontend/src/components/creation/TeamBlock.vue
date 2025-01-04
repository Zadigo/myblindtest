<template>
  <div class="card-body">
    <v-text-field v-model="requestData.name" placeholder="Team name" variant="solo-filled" flat />

    <v-btn variant="tonal" rounded @click="showAddPlayersModal=true">
      <FontAwesomeIcon class="me-2" icon="plus" /> Add players
    </v-btn>

    <v-btn variant="tonal" rounded @click="handleColorSelection">
      <FontAwesomeIcon class="me-2" icon="brush" /> Color
    </v-btn>

    <v-dialog v-model="showAddPlayersModal" persistent style="width:500px;">
      <v-card>
        <v-card-text>
          <v-text-field placeholder="Player name" variant="solo-filled" flat />
        </v-card-text>

        <v-card-actions>
          <v-btn variant="tonal" @click="showAddPlayersModal=false">
            <FontAwesomeIcon class="me-2" icon="check" /> Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts" setup>
import { Team } from '@/types';
import { computed, PropType, ref } from 'vue';

const emit = defineEmits({
  'update:team' (_data: Team) {
    return true
  },
  'select-color' (_team: Team) {
    return true
  }
})

const props = defineProps({
  team: {
    type: Object as PropType<Team>,
    default: () => ({
      name: '',
      score: 0,
      players: []
    })
  }
})

const showAddPlayersModal = ref(false)

const requestData = computed({
  get: () => props.team,
  set: (value) => {
    emit('update:team', value)
  }
})

function handleColorSelection () {
  emit('select-color', props.team)
}
</script>
