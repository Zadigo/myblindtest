<template>
  <volt-dialog v-model:visible="show" header="Connected devices" modal :dismissable-mask="false" class="w-96">
    <p class="mb-4">
      You have an active game session. Changing devices now may interrupt the game for connected players.
    </p>

    <div class="flex justify-end gap-2">
      <volt-button severity="tertiary" @click="show = false">
        Cancel
      </volt-button>

      <volt-button severity="danger" @click="emit('proceed')">
        Proceed
      </volt-button>
    </div>
  </volt-dialog>
</template>

<script setup lang="ts">
const props = defineProps<{ modelValue: boolean }>()
const emit = defineEmits<{ 'update:modelValue': [boolean], proceed: [] }>()
const show = useVModel(props, 'modelValue', emit)
</script>
