<template>
  <section class="site">
    <BaseNavbar />
    <Toaster position="top-right" />

    <section class="container my-5">
      <div class="row">
        <Transition name="opacity">
          <div v-if="!isStarted" class="col-sm-12 col-md-12">
            <div class="card shadow-sm mb-2">
              <div class="card-body">
                <BaseTabs />
              </div>
            </div>
          </div>
        </Transition>

        <RouterView />

        <div class="col-sm-12 col-md-6">
          <div class="card shadow-sm mb-2">
            <div class="card-body">
              <div class="infos d-flex align-items-center gap-2">
                <h3 v-if="cache" class="bg-secondary rounded-1 p-3 d-flex flex-column text-center">
                  {{ cache.currentStep }}
                  <span class="fw-light">song</span>
                </h3>

                <h3 class="bg-info rounded-1 p-3 d-flex flex-column text-center">
                  {{ firstTeamScore }}
                  <span class="fw-light">Team n°1</span>
                </h3>

                <h3 class="bg-info rounded-1 p-3 d-flex flex-column text-center">
                  {{ secondTeamScore }}
                  <span class="fw-light">Team n°2</span>
                </h3>
              </div>
            </div>
          </div>

          <div class="card shadow-sm">
            <div v-if="currentSong" class="card-body text-center">
              <iframe :src="currentSong.youtube" width="480" height="315" title="YouTube video player" frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; web-share" referrerpolicy="strict-origin-when-cross-origin" />
            </div>
          </div>
        </div>
      </div>
    </section>
  </section>
</template>

<script lang="ts" setup>
import { useHead } from 'unhead';
import { Toaster } from 'vue-sonner';

import BaseNavbar from '@/components/BaseNavbar.vue';
import BaseTabs from '@/components/BaseTabs.vue';
import { useSongs } from '@/stores/songs';
import { storeToRefs } from 'pinia';

useHead({
  title: 'Blind test'
})

const songsStore = useSongs()
const { cache, currentSong, firstTeamScore, secondTeamScore, isStarted } = storeToRefs(songsStore)
</script>

<style lang="scss" scoped>
.infos h3 {
  min-width: 100px;
}

.infos h3 span {
  font-size: 0.8rem;
}
</style>
