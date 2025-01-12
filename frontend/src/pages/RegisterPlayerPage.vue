<template>
  <section ref="sectionEl">
    <v-container>
      <v-row class="mt-16">
        <v-col cols="4" offset="4">
          <v-card>
            <v-card-text>
              <v-form @submit.prevent>
                <v-text-field variant="solo-filled" placeholder="Blind test ID" flat />
                <v-btn variant="tonal" color="dark" rounded>
                  Join blind test
                </v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';

// import { OTPInput } from 'vue-input-otp'

// const input = ref<string>('')

const sectionEl = ref<HTMLElement>()

onMounted(() => {
  if (sectionEl.value) {
    sectionEl.value.style.backgroundImage = `url('/registration.jpg')`
  }
})
</script>

<style lang="scss" scoped>
section {
  height: 100vh;
  background-position: center;
  background-repeat: no-repeat;
  background-position-y: -300px;
}
</style>
