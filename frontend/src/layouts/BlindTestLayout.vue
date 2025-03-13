<template>
  <div class="blind-test position-relative" style="z-index:1000;">
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
  </div>
</template>

<script lang="ts" setup>
import { useSongs } from '@/stores/songs';
import { useMediaQuery } from '@vueuse/core';
import { useHead } from 'unhead';
import { computed } from 'vue';

useHead({
  title: 'Blind test'
})

const isLargeScreen = useMediaQuery('(min-width: 1024px)')
console.log('isLargeScreen', isLargeScreen.value)

const songsStore = useSongs()

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
  return formatStyle('#e74c3c')
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

  /* Laptops and small screens */
  @media screen and (min-width: 769px) and (max-width: 1024px) {
    .video {
      left: 34%;
    }
  }

  /* Large screens and Desktops */
  @media screen and (min-width: 1025px) and (max-width: 1200px) {
    .video {
      left: 38%;
    }
  }

  /* TV and Extra Large Screens */
  @media screen and (min-width: 1201px) {
    .video {
      left: 34%;
    }
  }
}
</style>
