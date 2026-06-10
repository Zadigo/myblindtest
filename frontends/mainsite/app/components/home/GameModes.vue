<template>
  <volt-card>
    <template #title>
      <h3 class="font-bold">
        {{ $t('Game modes') }}
      </h3>
    </template>

    <template v-if="currentSettings" #content>
      <div class="py-3">
        <volt-label label-for="solo-mode" :label="$t('Run in solo mode')">
          <volt-toggle-switch id="solo-mode" v-model="currentSettings.settings.soloMode" />
        </volt-label>
      </div>

      <div class="py-3">
        <volt-label label-for="admin-plays" :label="$t('Admin is registered in a team')">
          <volt-toggle-switch id="admin-plays" v-model="currentSettings.settings.adminPlays" />
        </volt-label>
      </div>

      <!-- Epic Game Mode -->
      <div class="py-3">
        <volt-fieldset legend="Epic game mode">
          <div class="space-y-3">
            <grid-switch id="wrong-cost-points" v-model:switch-value="testRef">Every wrong answer costs points (which can depend on the difficulty of the song)</grid-switch>
            <grid-switch v-model:switch-value="testRef">The player who gives the right answer gains points and every other player loses a certain amount of points based on their ranking</grid-switch>
            <grid-switch v-model:switch-value="testRef">Players can multiply their points based on how fast they answer</grid-switch>
            <grid-switch v-model:switch-value="testRef">Players can multiply theirt points if they answer in a row without making mistakes</grid-switch>
            <grid-switch v-model:switch-value="testRef">Players can multiply their points if they answer a song which genre matches their favorite genre</grid-switch>
            <grid-switch v-model:switch-value="testRef">Players must obtain 5 points or more in each category to win the game</grid-switch>
          </div>
        </volt-fieldset>
      </div>
    </template>

    <template v-else #content>
      <div class="space-y-2">
        <volt-skeleton height="100px" />
        <volt-skeleton height="100px" />
      </div>
    </template>
  </volt-card>
</template>

<script setup lang="ts">
const { currentSettings } = useSession()
const testRef = ref(false)
</script>
