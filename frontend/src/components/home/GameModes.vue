<template>
  <Card class="border-0 shadow-md">
    <CardHeader>
      <CardTitle>
        Game modes
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
