<template>
  <ion-page>
    <!-- Content -->
    <ion-content class="ion-padding">
      <ion-grid>
        <ion-row>
          <ion-col size="8" offset="2" class="ion-justify-content-center">
            <score :animate-score="animateScore" class="mt-6 mb-3" />
          </ion-col>

          <ion-col size="12">
            <div class="h-auto w-auto">
              <div class="relative h-auto w-full">
                <div ref="buzzEl" class="absolute top-0 left-0 h-[330px] w-[330px] bg-red-500 rounded-full" />
                <div ref="buzzEl" class="absolute top-4 left-4 h-[300px] w-[300px] bg-red-600 rounded-full shadow-2xl border-5 border-red-400" @click="handleBuzz" />
              </div>
            </div>
          </ion-col>
        </ion-row>
      </ion-grid>
    </ion-content>

    <!-- Loading -->
    <ion-loading :is-open="isConnecting" message="Trying connection..." />
  </ion-page>
</template>

<script setup lang="ts">
const buzzerStore = useBuzzerStore()
const { buzzCounter } = storeToRefs(buzzerStore)

const isConnecting = ref<boolean>(false)

const buzzEl = shallowRef<HTMLElement>()
const animateScore = ref<boolean>(false)

const ws = useWebSocket('/ws/buzz', {
  immediate: false
})

watch(() => ws.status.value === 'OPEN', (newValue) => {
  if (newValue) {
    isConnecting.value = true
    buzzEl.value?.classList.add('active')
  } else {
    isConnecting.value = false
    buzzEl.value?.classList.remove('active')
  }
})

/**
 * Handle the buzz action
 */
function handleBuzz() {
  if (buzzEl.value) {
    buzzEl.value.classList.add('active')
    buzzerStore.increment()
    animateScore.value = true
    
    setInterval(() => {
      buzzEl.value?.classList.remove('active')
    }, 800)

    setTimeout(() => {
      animateScore.value = false
    }, 1000)
  }
}

onMounted(() => {
  ws.open()
})

onBeforeUnmount(() => {
  // isConnecting.value = true
  ws.close()
})
</script>
