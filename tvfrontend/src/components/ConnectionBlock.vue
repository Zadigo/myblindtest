<template>
  <div class="w-4/12 mx-auto mt-20">
    <VoltCard>
      <template #content>
        <form class="flex-col justify-center items-center space-y-5 w-full" @submit.prevent>
          <VoltInputOtp v-model="code" />

          <VoltButton variant="secondary" class="self-end" size="lg" @click="emit('connect-client', code)">
            Se connecter
          </VoltButton>
        </form>
      </template>
    </VoltCard>
  </div>
</template>

<script setup lang="ts">
const code = ref<string>('')

const emit = defineEmits<{
  'connect-client': [value: string]
}>()
</script>
