<template>
  <div class="col-sm-12 col-md-6">
    <div class="card shadow-sm">
      <TeamBlock v-for="(team, i) in cache.teams" :key="i" :team="team" @select-color="handleColorSelection" />
    </div>

    <v-dialog v-model="showChooseColor" style="width:500px;">
      <v-card>
        <v-card-text>
          <div class="row">
            <div class="col-12 d-flex justify-content-center">
              <VueColorWheel v-model:color="wheelColor" wheel="aurora" harmony="monochromatic" :radius="160" :default-color="wheelColor" @change="handleChangeColors" />
            </div>

            <div class="col-12 mt-4">
              <v-text-field v-model="wheelColor" variant="solo-filled" flat />
            </div>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { useSongs } from '@/stores/songs';
import { Team } from '@/types';
import { useDebounce } from '@vueuse/core';
import { storeToRefs } from 'pinia';
import { ref, watch } from 'vue';
import type { Harmony } from 'vue-color-wheel';
import { VueColorWheel } from 'vue-color-wheel';

import TeamBlock from '@/components/TeamBlock.vue';

const songsStore = useSongs()
const { cache } = storeToRefs(songsStore)

const selectedTeam = ref<Team>()
const showChooseColor = ref(false)

const wheelColor = useDebounce(ref('#40ffff'))
const colorList = ref<Harmony[]>()

watch(wheelColor, (newValue) => {
  if (selectedTeam.value) {
    selectedTeam.value.color = newValue
  }
})

function handleColorSelection (team: Team) {
  selectedTeam.value = team
  showChooseColor.value = true
}

function handleChangeColors (harmonyColors: Harmony[]) {
  colorList.value = harmonyColors
}
</script>
