<template>
  <div class="my-30 text-center">
    <div class="mb-10">
      <h1 class="text-7xl font-bold text-primary-200 animate transition-colors animate-pulse">
        Blind test
      </h1>

      <p class="w-80 mt-2 text-primary-400">
        Lorem ipsum dolor sit amet consectetur, adipisicing elit.
      </p>
    </div>

    <volt-card>
      <template #content>
        <div v-if="!isConnected" class="p-5 rounded-md bg-primary-200 mb-5">
          Error: No connection
        </div>

        <form class="flex-col justify-center space-y-5 text-center" @submit.prevent>
          <div class="mx-auto">
            <!-- <volt-input-otp v-model="code" /> -->
            <volt-input-text v-model="code" class="w-full" placeholder="Connection code" />
          </div>

          <div class="w-auto">
            <volt-button :disabled="code === '' || code === null" variant="secondary" class="self-end" size="lg" @click="goToScores">
              Se connecter
            </volt-button>
          </div>
        </form>
      </template>
    </volt-card>
  </div>
</template>

<script setup lang="ts">
/**
 * Connection
 */

const connectionStore = useConnectionStore()
const { code, isConnected } = storeToRefs(connectionStore)


const router = useRouter()

function goToScores() {
  router.push({ name: 'ScoresPage' })
}
</script>
