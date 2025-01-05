<template>
  <div class="blind-test position-relative">
    <div class="teams">
      <div class="team bg-light">
        <slot name="teamOne" />
      </div>
      
      <div :style="teamStyles" class="team">
        <slot name="teamTwo" />
      </div>

      <!-- Video -->
      <slot name="video" />
    </div>

    <slot />

    <v-dialog v-model="showBlindtestSettings" persistent style="width:500px;">
      <v-card>
        <v-card-text>
          Settings
        </v-card-text>

        <v-card-actions>
          <v-btn variant="text" @click="showBlindtestSettings=false">
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts" setup>
import { useSongs } from '@/stores/songs';
import { useHead } from 'unhead';
import { computed, ref } from 'vue';

useHead({
  title: 'Blind test'
})

const songsStore = useSongs()
const showBlindtestSettings = ref(false)


function formatStyle (value: string | null) {
  if (value) {
    return `background-color: ${value};`
  } else {
    return ''
  }
}

const teamStyles = computed(() => {
  if( songsStore.cache) {
    if (songsStore.cache.teams[1].color) {
      return formatStyle(songsStore.cache.teams[1].color)
    }
  }
  return formatStyle('#48a9a6')
})
</script>

<style lang="scss">
%score {
  width: 100px;
  height: auto;
  min-height: 10px;
  text-align: center;
}

.blind-test {
  .teams {
    height: 100vh;
    width: 100%;
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr;

    .team {
      padding: 1rem;
    }
  
    .score {
      @extend %score;
    }
  }

  .video {
    position: absolute;
    top: 10%;
    min-width: 420px;
    height: auto;
    left: 34%;
  }
}
</style>
