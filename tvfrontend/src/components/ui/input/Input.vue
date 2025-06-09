<script setup lang="ts">
import { inputVariants, type InputVariants } from '.'
import { cn } from '@/lib/utils'
import { useVModel } from '@vueuse/core'

import type { HTMLAttributes } from 'vue'

interface Props {
  defaultValue?: string | number
  modelValue?: string | number
  class?: HTMLAttributes['class']
  variant?: InputVariants['variant']
}

const props = defineProps<Props>()

const emits = defineEmits<{
  (e: 'update:modelValue', payload: string | number): void
}>()

const modelValue = useVModel(props, 'modelValue', emits, {
  passive: true,
  defaultValue: props.defaultValue,
})
</script>

<template>
  <input v-model="modelValue" data-slot="input" :class="cn(inputVariants({ variant }), props.class)">
</template>
