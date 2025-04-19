<template>
  <div class="container position-relative">
    <v-btn @click="selectRandom">
      Show
    </v-btn>

    <v-btn @click="testCacheUpdates">
      Cache
    </v-btn>

    {{ teamOneCards }}
    {{ availableCards.length }}

    <v-row>
      <v-col cols="5">
        <div class="team-slots">
          <div v-for="item in teamOneCards" :key="item.name" class="item">
            {{ item.name }}
          </div>
        </div>
      </v-col>
    </v-row>

    <Transition class="animate__animated animate__fast" enter-active-class="animate__slideInLeft animate__rubberBand" leave-active-class="animate__slideOutRight" @after-enter="onAfterEnter" @before-laave="onBeforeLeave">
      <v-card v-if="showCard" ref="cardEl" class="combat-card" @click="handleRandom">
        <v-card-text>
          <!-- <v-img src="/registration.jpg" /> -->
          <div v-if="selectedCard" class="fs-1">
            {{ selectedCard.name }}
          </div>
        </v-card-text>
      </v-card>
    </Transition>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue'
import { useWebSocket } from '@vueuse/core'
import { getBaseUrl } from '@/plugins/client'
import { useWebsocketUtilities } from '@/composables/utils'

interface Card {
  name: string
  team: number | null
  trashed: boolean
}

const cardEl = ref<HTMLElement>()
const showCard = ref(false)
const cardIndex = ref<number | null>(null)

const randomCards = ref<Card[]>([
  {
    name: '1x',
    team: null,
    trashed: false
  },
  {
    name: '2x',
    team: null,
    trashed: false
  },
  {
    name: '3x',
    team: null,
    trashed: false
  },
  {
    name: '4x',
    team: null,
    trashed: false
  },
  {
    name: '5x',
    team: null,
    trashed: false
  }
])

const availableCards = computed(() => {
  return randomCards.value.filter(x => x.team === null)
})

const selectedCard = computed(() => {
  if (cardIndex.value) {
    return randomCards.value[cardIndex.value]
  } else {
    return null
  }
})

const teamOneCards = computed(() => {
  return randomCards.value.filter(x => x.team === 1)
})

function selectRandom() {
  if (availableCards.value.length === 0) {
    return
  }

  cardIndex.value = Math.floor(Math.random() * availableCards.value.length)
  showCard.value = true
}

function handleRandom() {
  if (selectedCard.value) {
    selectedCard.value.team = 1
  }
  showCard.value = false
}

function onAfterEnter(el: HTMLElement) {
  el.classList.add('animate__animated', 'animate__swing')
}

function onBeforeLeave(el: HTMLElement) {
  el.classList.remove('animate__animated', 'animate__swing')
  el.classList.add('animate__animated', 'animate__swing')
}

// TEST
const id = ref()
const ws = useWebSocket(getBaseUrl('/ws/connect', null, true), {
  immediate: false,
  onMessage() {
    id.value = ws.data.value.device_id
    console.log(ws.data.value)
  }
})

const { sendMessage } = useWebsocketUtilities()

function testCacheUpdates() {
  ws.open()
  ws.send(sendMessage({
    action: 'update_device_cache',
    device_id: id.value
  }))
}
</script>

<style lang="scss" scoped>
.combat-card {
  position: absolute;
  width: 300px;
  height: auto;
  top: 30%;
  left: 20%;
}

.team-slots {
  display: grid;
  grid-template-columns: repeat(3, 1fr);

  .item {
    height: 100px;
    width: 100px;
    background-color: grey;
  }
}
</style>
