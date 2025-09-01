<template>
  <div class="flex justify-between items-center">
    <div v-if="currentSong">
      <p class="font-bold">
        {{ currentSong.name }} <span class="font-semibold">({{ currentSong.artist.name }})</span>
      </p>

      <div class="inline-flex gap-1 my-2">
        <template v-for="i in 5" :key="i">
          <vue-icon v-if="i <= currentSong.difficulty" icon="fa-solid:star" />
          <vue-icon v-else icon="fa-solid:star" class="text-slate-50" />
        </template>
      </div>

      <div>
        <volt-badge variant="default">
          {{ currentSong.genre }}
        </volt-badge>
      </div>
    </div>

    <div class="flex justify-end gap-2 items-center">
      <volt-secondary-button variant="outline">
        <router-link :to="{ name: 'home' }">
          <vue-icon icon="fa-solid:home" size="15" />
        </router-link>
      </volt-secondary-button>

      <volt-button variant="outline" @click="() => emit('show:wheel')">
        <vue-icon icon="fa-solid:bolt" size="15" />
      </volt-button>
    </div>
  </div>

</template>

<script setup lang="ts">
import type { Song } from '@/types'

defineProps<{ currentSong: Song | undefined }>()
const emit = defineEmits<{ 'show:wheel': [] }>()
</script>
