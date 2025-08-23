<template>
  <div class="w-4/12 mx-auto mt-20">
    <volt-card>
      <template #content>
        <form class="flex-col justify-center space-y-5 text-center" @submit.prevent>
          <div class="mx-auto">
            <volt-input-otp v-model="code" />
          </div>

          <div class="w-auto">
            <volt-button variant="secondary" class="self-end" size="lg" @click="emit('check-code', code)">
              Se connecter
            </volt-button>
          </div>
        </form>
      </template>
    </volt-card>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits<{ 'check-code': [value: string] }>()
const code = ref<string>('')
</script>
