<template>
  <blind-test-layout>
    <template #teamOne>
      <team-block :team-index="0" class="bg-primary/40" />
    </template>

    <template #teamTwo>
      <team-block :team-index="1" block-position="ms-auto" class="bg-primary/20" />
    </template>

    <template #video>
      <video-block ref="videoEl" />
    </template>
  </blind-test-layout>
</template>

<script setup lang="ts">
import type VideoBlock from '@/components/blindtest/VideoBlock.vue'
import type { VideoBlockExposedMethods } from '@/types'

const videoEl = useTemplateRef<InstanceType<typeof VideoBlock> & VideoBlockExposedMethods>('videoEl')

/**
 * Wescocket
 */

const { wsObject } = useGameWebsocket()
onMounted(() => { wsObject.open() })

/**
 * SEO
 */

useHead({
  title: 'Blindtest',
  meta: [
    {
      name: 'description',
      content: 'Play an exciting blindtest game with your friends! Guess the songs and compete for the highest score.'
    }
  ]
})
</script>
