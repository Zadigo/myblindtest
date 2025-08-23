<template>
  <ion-tabs>
    <!-- Router -->
    <ion-router-outlet />

    <!-- Tabs -->
    <ion-tab-bar slot="bottom">
      <ion-tab-button tab="home" href="/">
        <ion-icon :icon="home" />
      </ion-tab-button>

      <ion-tab-button tab="about" href="/about">
        <ion-icon :icon="informationCircleOutline" />
      </ion-tab-button>
      
      <ion-tab-button tab="account" href="/account">
        <ion-icon :icon="personOutline" />
      </ion-tab-button>
    </ion-tab-bar>
  </ion-tabs>
</template>

<script setup lang="ts">
import { home, informationCircleOutline, personOutline } from 'ionicons/icons'
</script>
