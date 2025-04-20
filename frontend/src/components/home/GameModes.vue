<template>
  <Card class="border-0 shadow-md">
    <CardHeader>
      <CardTitle>
        Game modes
      </CardTitle>
    </CardHeader>

    <CardContent>
      <v-switch v-model="songStore.cache.settings.soloMode" label="Run in solo mode" inset hide-details />
      <v-switch v-model="songStore.cache.settings.adminPlays" label="Admin is registered in a team" inset hide-details />
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { useSongs } from '@/stores/songs'

const songStore = useSongs()
</script>
