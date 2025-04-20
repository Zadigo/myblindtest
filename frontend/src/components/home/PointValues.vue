<template>
  <Card class="border-0 shadow-md my-2">
    <CardHeader>
      <CardTitle>
        Point value and bonuses
      </CardTitle>
    </CardHeader>

    <CardContent>
      <form @submit.prevent>
        <v-text-field v-model.number="songStore.cache.settings.pointValue" type="number" min="1" placeholder="Point value" variant="solo-filled" flat />
        <v-switch v-model="songStore.cache.settings.songDifficultyBonus" label="Use song difficulty bonus" inset hide-details />

        <v-divider class="my-2" />

        <v-switch v-model="songStore.cache.settings.speedBonus" label="Use answering speed bonus" inset hide-details />
      </form>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { useSongs } from '@/stores/songs'

const songStore = useSongs()
</script>
