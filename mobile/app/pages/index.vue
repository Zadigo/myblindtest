<template>
  <ion-page>
    <ion-content ion="padding">
      <ion-row class="mt-6">
        <ion-col size="12" class="ion-margin-top">
          <ion-card>            
            <ion-card-content>
              <ion-input v-model="username" placeholder="Username" />
              <ion-input v-model="preferredGenre" placeholder="Preferred genre" />
            </ion-card-content>
          </ion-card>

          <ion-card>            
            <ion-card-content>
              <ion-input-otp v-model="code" />

              <div class="ion-text-center ion-margin-top">
                <ion-button expand="block" color="primary" href="/buzzer">
                  Start
                </ion-button>
              </div>
            </ion-card-content>
          </ion-card>
        </ion-col>
      </ion-row>

    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
const username = ref<string>('')
const preferredGenre = ref<string>('')
const code = ref<string>('')

</script>
