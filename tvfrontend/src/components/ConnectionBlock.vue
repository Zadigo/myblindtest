<template>
  <div class="w-4/12 mx-auto mt-20">
    <Card class="border-none shadow-md">
      <CardContent>
        <form class="flex flex-col" @submit.prevent>
          <Input v-model="code" class="bg-slate-100 rounded-sm w-full p-6 mb-4" />
          <Button variant="secondary" class="self-end" size="lg" @click="emit('connect-client', code)">
            Se connecter
          </Button>
        </form>
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
const code = ref<string>('')

const emit = defineEmits({
  'connect-client'(_value: string) {
    return true
  }
})
</script>
