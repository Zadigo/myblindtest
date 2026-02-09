<template>
  <volt-container size="sm">
    <div class="flex items-center justify-center h-screen">
      <h1 class="text-3xl text-primary-50">En attente de connexion...</h1>
      <!-- <base-game-loader /> -->
      <nuxt-link :to="`/blindtest/player/game?id=${query.id}&player=${query.player}`">
        Game
      </nuxt-link>
    </div>
  </volt-container>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'player'
})

const { wsObject, query } = usePlayerWebsocket()
wsObject.open()
</script>
