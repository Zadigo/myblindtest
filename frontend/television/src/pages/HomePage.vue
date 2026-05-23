<template>
  <div class="my-30 text-center max-w-md text-centers mx-auto">
    <div class="mb-10">
      <h1 class="text-7xl font-bold text-primary-200 animate transition-colors animate-pulse">
        Blind test
      </h1>

      <p class="w-80 mx-auto mt-2 text-primary-400">
        Lorem ipsum dolor sit amet consectetur, adipisicing elit.
      </p>
    </div>

    <volt-card>
      <template #content>
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

/**
 * Websocket
 */

const router = useRouter()
const { connect, checkPinCode } = useGameWebsocket()

function goToScores() {
  checkPinCode(code.value)
  router.push({ name: 'scores', query: { code: code.value } })
}

/**
 * Lifecycle
 */

const tokens = ['h-screen', 'bg-no-repeat', 'bg-gradient-to-b', 'from-primary-100', 'to-primary-50']

onMounted(() => {
  document.body.classList.add(...tokens)
  connect()
})

onUnmounted(() => {
  document.body.classList.remove(...tokens)
})
</script>
