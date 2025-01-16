<template>
  <IonHeader>
    <IonToolbar>
      <IonTitle>
        Home
      </IonTitle>
    </IonToolbar>
  </IonHeader>
  <IonContent>
    <IonGrid>
      <IonRow class="mt-6">
        <IonCol size="12" class="ion-margin-top">
          <IonCard>
            <IonCardHeader>
              <IonCardTitle>
                Page d'acceuil
              </IonCardTitle>
            </IonCardHeader>
            <IonCardContent>
              <IonInput placeholder="Username" />
              <IonInput placeholder="Preferred genre" />
              <IonInput placeholder="Code" />
              
              <div class="ion-text-center ion-margin-top">
                <IonNavLink router-direction="forward" :component="buzzComponent">
                  <IonButton>
                    Start Blintest
                  </IonButton>
                </IonNavLink>
              </div>
            </IonCardContent>
          </IonCard>
        </IonCol>
      </IonRow>
    </IonGrid>
  </IonContent>
</template>

<script setup lang="ts">
import BuzzContainer from '@/components/BuzzContainer.vue';
import { IonButton, IonCard, IonCardContent, IonCol, IonContent, IonHeader, IonGrid, IonInput, IonNavLink, IonRow, IonTitle, IonToolbar, IonCardHeader, IonCardTitle } from '@ionic/vue';
import { ref } from 'vue';

const buzzComponent = ref(BuzzContainer)
</script>
