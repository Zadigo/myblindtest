<template>
  <volt-container size="sm">
    <div class="flex items-center justify-center h-screen">
      <h1 class="text-3xl text-primary-50">En attente de connexion...</h1>
      <base-game-loader />
    </div>
  </volt-container>
</template>

<script setup lang="ts">
const { wsObject } = usePlayerWebsocket()
wsObject.open()
</script>
