<template>
  <section class="container my-5">
    <div class="row">
      <div class="col-md-6 col-sm-12">
        <div class="card">
          <div class="card-body">
            <v-text-field v-model="teamOne.name" placeholder="Team name" variant="solo-filled" flat />
          </div>
        </div>
      </div>

      <div class="col-md-6 col-sm-12">
        <div class="card">
          <div class="card-body">
            <v-text-field v-model="teamTwo.name" placeholder="Team name" variant="solo-filled" flat />
          </div>
        </div>
      </div>

      <div class="col-md-6 col-sm-12 offset-md-3 mt-3">
        <div class="card">
          <div class="card-body">
            <div class="d-flex gap-2">
              <v-btn :active="selectedTeam===1" variant="tonal" @click="selectedTeam=1">
                Team 1
              </v-btn>

              <v-btn :active="selectedTeam===2" variant="tonal" @click="selectedTeam=2">
                Team 2
              </v-btn>
            </div>
            
            <div class="d-flex justify-content-center mb-4">
              <VueColorWheel v-model:color="wheelColor" wheel="aurora" harmony="complementary" :radius="160" :default-color="wheelColor" @change="handleChangeColor" />
            </div>
            <v-text-field v-model="wheelColor" variant="solo-filled" flat />
          </div>

          <div class="card-footer">
            <v-btn to="/">
              Back to settings
            </v-btn>
            <v-btn to="/blind-test">
              Go to blindtest
            </v-btn>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useSongs } from '@/stores/songs';
import { useDebounce } from '@vueuse/core';
import { useHead } from 'unhead';
import { computed, onBeforeMount, ref, watch } from 'vue';

import type { Harmony } from 'vue-color-wheel';
import { VueColorWheel } from 'vue-color-wheel';

useHead({
  title: 'Réglages'
})

const songsStore = useSongs()
const wheelColor = useDebounce(ref<string>('#5a228b'))

const selectedTeam = ref(1)
const colorList = ref<Harmony[]>()

const teamOne = computed(() => {
  return songsStore.cache.teams[0]
})

const teamTwo = computed(() => {
  return songsStore.cache.teams[1]
})

watch(wheelColor, (newValue) => {
  if (selectedTeam.value === 1) {
    songsStore.cache.teams[0].color = newValue
  } else {
    songsStore.cache.teams[1].color = newValue
  }
})

function handleChangeColor (harmonyColors: Harmony[]) {
  colorList.value = harmonyColors
}

onBeforeMount(() => {
  wheelColor.value = '#e74c3c'
})
</script>
