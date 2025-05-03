<template>
  <section class="h-auto relative">
    <div class="grid grid-cols-2 grid-rows-1">
      <div id="left" class="bg-blue-200 h-full p-5 h-scren">
        <div id="team" class="flex-col justify-start w-7/12">
          <Card class="w-full text-center">
            <CardContent>
              <h1 class="text-5xl font-bold">
                25
              </h1>

              <p class="font-light uppercase">
                Points
              </p>
            </CardContent>
          </Card>

          <Card class="mt-2 mb-10">
            <CardContent>
              <div class="flex justify-center gap-2">
                <Button variant="secondary">
                  <VueIcon name="fa-solid:t" />
                  Title
                </Button>

                <Button variant="secondary">
                  <VueIcon name="fa-solid:a" />
                  Artist
                </Button>

                <Button variant="secondary">
                  <VueIcon name="fa-solid:t" />
                  Both
                </Button>
              </div>

              <div class="flex justify-center mt-4 w-full">
                <Button class="w-8/12 self-center" variant="default">
                  Validate
                </Button>
              </div>
            </CardContent>
          </Card>

          <div class="flex gap-1 justify-center p-5 mt-3">
            <div v-for="i in 5" :key="i" class="p-2 bg-yellow-100 rounded-md w-1/6" />
          </div>

          <Transition class="animate__animated" enter-to-class="animate__zoomInLeft" leave-to-class="animate__fadeOutLeft">
            <h1 v-if="hasConsecutiveAnswers" class="text-5xl font-bold text-gray-700">
              Exceptionnel x 1
            </h1>
          </Transition>

          <!-- Fireworks -->
          <BaseFireworks v-show="gameStarted && hasConsecutiveAnswers" />
        </div>
      </div>

      <div id="right" class="bg-yellow-200 p-5 h-screen">
        ...
      </div>

      <div class="absolute my-10 left-2/6 w-4/12">
        <Card class="border-none shadow-md">
          <CardHeader>
            <div class="flex justify-end gap-2">
              <Button variant="outline">
                <VueIcon icon="fa-solid:home" size="15" />
              </Button>

              <Button variant="outline" @click="showRandomizer=!showRandomizer">
                <VueIcon icon="fa-solid:bolt" size="15" />
              </Button>
            </div>
          </CardHeader>

          <!-- Video -->
          <CardContent>
            <div id="video-wrapper" class="rounded-md overflow-hidden flex justify-center items-center max-w-full">
              <iframe :src="'https://www.youtube.com/embed/CByuJoBwvbE?si=0jTKuldFoTmZYYf0'" class="max-w-full h-auto block" width="400" height="200" title="Sinéad O&#39;Connor - Nothing Compares 2 U (Official Music Video) [HD]" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" />
            </div>
          </CardContent>

          <CardContent v-if="showRandomizer">
            <GenreRandomizer ref="randomizerEl" :items="wheelDetaults" @completed="randomizerComplete" />
          </CardContent>

          <CardFooter>
            <div class="inline-flex justify-center w-full gap-1">
              <Button variant="outline">
                <VueIcon icon="fa-solid:stop" size="15" />
                Stop
              </Button>

              <Button variant="outline">
                <VueIcon icon="fa-solid:play" size="15" />
                Start
              </Button>

              <Button variant="destructive">
                <VueIcon icon="fa-solid:exclamation" size="15" />
                Wrong answer
              </Button>
            </div>
          </CardFooter>
        </Card>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { wheelDetaults } from '@/data'

import { ref } from 'vue'

const showRandomizer = ref<boolean>(false)
const gameStarted = ref<boolean>(false)
const hasConsecutiveAnswers = ref<boolean>(true)

/**
 *
 */
function randomizerComplete() {
  // DO something
}
</script>
