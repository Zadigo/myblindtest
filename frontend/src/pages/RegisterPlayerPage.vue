<template>
  <div class="container">
    <div class="row my-5">
      <div class="col-12">
        <OTPInput v-slot="{ slots }" v-model="input" :maxlength="6">
          <Slot v-for="(slot, i) in slots.slice(3)" v-bind="slot" :key="i" />
        </OTPInput>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { OTPInput } from 'vue-input-otp'

const input = ref<string>('')
</script>
