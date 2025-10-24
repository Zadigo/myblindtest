
<template>
  <Accordion unstyled :pt="theme" :ptOptions="{ mergeProps: ptViewMerge }">
    <slot />
  </Accordion>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ptViewMerge } from './utils'

import Accordion, { type AccordionPassThroughOptions, type AccordionProps } from 'primevue/accordion'

interface Props extends /* @vue-ignore */ AccordionProps {}
defineProps<Props>()

const theme = ref<AccordionPassThroughOptions>({
  root: ``
})
</script>
