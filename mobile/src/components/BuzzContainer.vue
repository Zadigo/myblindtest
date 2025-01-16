<template>
  <IonHeader>
    <IonToolbar>
      <IonButtons slot="secondary">
        <IonNavLink router-direction="root" :component="homeComponent">
          <IonButton fill="outline">
            <IonIcon slot="start" :icon="caretBack" />
          </IonButton>
        </IonNavLink>
      </IonButtons>
      <IonTitle>
        Buzzer
      </IonTitle>
    </IonToolbar>
  </IonHeader>
  <IonContent :fullscreen="true">
    <div class="bg-lighta">
      <IonGrid>
        <IonRow>
          <IonCol size="8" offset="2" class="ion-justify-content-center">
            <IonSpinner name="lines-sharp" />
            <ScoreBlock :animate-score="animateScore" class="mt-6 mb-3" />
          </IonCol>
          <IonCol size="12">
            <div class="buzzer">
              <div ref="buzzEl" class="buzz" @click="handleBuzz" />
            </div>
          </IonCol>
          <IonCol size="12">
            <IonNavLink router-direction="back" :component="homeComponent">
              <IonButton>
                Back
              </IonButton>
            </IonNavLink>
          </IonCol>
        </IonRow>
      </IonGrid>

      <IonButton @click="isopen=true">Test</IonButton>
    </div>

    <IonActionSheet :is-open="isopen" header="Actions" :buttons="actionSheetButtons" @didDismiss="isopen=false" />
  </IonContent>
</template>

<script setup lang="ts">
import 'animate.css';

// import { useWebSocket } from '@vueuse/core';
import { useSongs } from '@/stores/songs';
import { IonButton, IonButtons, IonCol, IonContent, IonGrid, IonActionSheet, IonHeader, IonIcon, IonNavLink, IonRow, IonSpinner, IonTitle, IonToolbar } from '@ionic/vue';
import { caretBack } from 'ionicons/icons';
import { storeToRefs } from 'pinia';
import { markRaw, onBeforeUnmount, onMounted, ref, shallowRef } from 'vue';

import HomeComponent from '@/components/HomeComponent.vue';
import { useWebSocket } from '@vueuse/core';

import ScoreBlock from './ScoreBlock.vue';

const songStore = useSongs()
const { buzzCounter } = storeToRefs(songStore)

const homeComponent = markRaw(HomeComponent)

const actionSheetButtons = [
  {
    text: 'Delete',
    role: 'destructive',
    data: {
      action: 'delete',
    },
  },
  {
    text: 'Share',
    data: {
      action: 'share',
    },
  },
  {
    text: 'Cancel',
    role: 'cancel',
    data: {
      action: 'cancel',
    },
  },
];

const isopen = ref(false)
const buzzEl = shallowRef<HTMLElement>()
const animateScore = ref<boolean>(false)

const ws = useWebSocket('/ws/buzz', {
  immediate: false
})

function handleBuzz() {
  if (buzzEl.value) {
    buzzEl.value.classList.add('active')
    buzzCounter.value += 1
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
  isopen.value = true
  ws.close()
})
</script>

<style lang="scss">
$red: rgba(159, 15, 23, 1);
$red_on: #dc0d29;
$size: 300px;

.buzzer {
  position: relative;

  .buzz {
    // position: absolute;
    // top: -50%;
    // left: 50%;
    height: $size;
    width: $size;
    margin: auto;
    padding: 0px;
    background-color: $red;
    border-radius: 100%;
    border: 20px solid #222;
    box-shadow: 0px 0px 10px #111;
    text-align: center;
    transition: background-color 0.15s ease-in-out;
  
    &.active {
      background-color: $red_on;
    }
  }
}
</style>
