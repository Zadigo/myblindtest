<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Home</ion-title>
        <IonProgressBar type="indeterminate" />
      </ion-toolbar>
    </ion-header>
    <ion-content :fullscreen="true">
      <!-- <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">Home</ion-title>
        </ion-toolbar>
      </ion-header> -->

      <ion-fab slot="fixed" vertical="top" horizontal="end">
        <ion-fab-button>
          <ion-icon :icon="chevronForwardCircle"></ion-icon>
        </ion-fab-button>
      </ion-fab>
      
      <IonNav :root="homeComponent" />
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { IonContent, IonHeader, IonPage, IonFab, IonFabButton, IonIcon, IonTitle, IonToolbar, IonNav, IonProgressBar } from '@ionic/vue';
import { chevronForwardCircle } from 'ionicons/icons'
import { markRaw } from 'vue';

import HomeComponent from '@/components/HomeComponent.vue';

const homeComponent = markRaw(HomeComponent)
</script>
