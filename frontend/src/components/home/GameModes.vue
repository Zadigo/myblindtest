<template>
  <Card class="border-0 bg-brand-shade-3/30 shadow-none">
    <CardHeader>
      <CardTitle>
        <h3 class="font-bold">
          Game modes
        </h3>
      </CardTitle>
    </CardHeader>

    <CardContent>
      <div class="py-3">
        <Label>
          <Switch v-model="songStore.cache.settings.soloMode" />
          Run in solo mode
        </Label>
      </div>

      <div class="py-3">
        <Label>
          <Switch v-model="songStore.cache.settings.adminPlays" />
          Admin is registered in a team
        </Label>
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { useSongs } from '@/stores/songs'

const songStore = useSongs()
</script>
