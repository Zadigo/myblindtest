<template>
  <volt-card>
    <template #title>
      <h3 class="font-bold">
        Epic game mode
      </h3>
    </template>

    <template #content>
      <div class="grid grid-cols-3">
        <div v-for="idx in 10" :key="idx" class="border border-primary-500 rounded-xl">
          1
        </div>
      </div>
    </template>
  </volt-card>
</template>
