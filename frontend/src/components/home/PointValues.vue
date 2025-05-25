<template>
  <Card class="border-0 shadow-md">
    <CardHeader>
      <CardTitle>
        Point value and bonuses
      </CardTitle>
    </CardHeader>

    <CardContent>
      <Input v-model.number="songStore.cache.settings.pointValue" type="number" min="1" placeholder="Point value" />

      <div class="py-3">
        <Label>
          <Switch v-model="songStore.cache.settings.songDifficultyBonus" />
          Use song difficulty bonus
        </Label>
      </div>

      <div class="py-3">
        <Label>
          <Switch v-model="songStore.cache.settings.speedBonus" />
          Use answering speed bonus
        </Label>
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
const songStore = useSongs()
</script>
