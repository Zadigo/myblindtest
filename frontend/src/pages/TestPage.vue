<template>
  <div class="blind-test position-relative">
    <div class="teams">
      <div class="team first-team bg-light">
        <div class="d-flex flex-column align-items-center" style="margin-right:10rem;">
          <div class="p-3 bg-light">
            <h1 class="h4 fw-bold m-0 d-flex align-items-center gap-2">
              Team 1
            </h1>
          </div>
          
          <div ref="scoreBoxEl" class="score p-3 rounded-3 bg-primary" style="width: 200px;">
            <h2 class="fs-1 w bold m-0">
              34
            </h2>

            <p class="m-0 fw-light text-lowercase">
              Points
            </p>
          </div>

          <div class="mt-5 d-flex align-items-center flex-column gap-2">
            <v-btn variant="tonal" color="blue-darken-4" size="x-large" rounded @click="handleAnswer">
              <FontAwesomeIcon icon="check" class="me-2" /> Correct answer
            </v-btn>

            <v-btn variant="tonal" color="dark" rounded @click="showTeamSettings=true">
              <FontAwesomeIcon icon="cog" />
            </v-btn>
          </div>
        </div>
      </div>
      
      <div class="team second-team bg-dark">
        Team 2
      </div>

      <!-- Video -->
      <div class="video">
        <div class="card">
          <div class="card-header border-bottom-0">
            <div class="row">
              <div class="col-12 d-flex justify-content-between">
                <div class="col-auto">
                  <div class="mb-1 badge fs-5 text-bg-primary p-2">
                    0/-
                  </div>
                </div>

                <div class="col-auto">
                  <v-btn variant="tonal" color="dark" rounded @click="showTeamSettings=true">
                    <FontAwesomeIcon icon="cog" />
                  </v-btn>
                </div>
              </div>

              <div class="col-12">
                <h4 class="h5 mt-4 mb-1">
                  Song name
                </h4>

                <div class=" mb-1 fw-light d-flex align-items-center gap-2">
                  <span>Artist name</span>
                  <span class="badge text-bg-secondary">
                    Pop rock
                  </span>
                </div>
                
                <v-rating :length="5" :model-value="3" :size="22" color="blue-darken-1" readonly />
              </div>
            </div>
          </div>

          <div class="card-body">
            <!-- https://www.youtube.com/embed/0-EF60neguk -->
            <iframe width="400" height="200" src="https://www.youtube.com/embed/0-EF60neguk" title="Sinéad O&#39;Connor - Nothing Compares 2 U (Official Music Video) [HD]" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" :onYouTubeIframeAPIReady="handleIframeLoaded" />
            <div class="text-center">
              <span class="loader-7" />
            </div>
          </div>

          <div class="card-footer d-flex justify-content-between align-items-center">
            <div class="actions">
              <!-- <v-btn variant="tonal">
                Start
              </v-btn> -->

              <v-btn variant="tonal">
                Stop
              </v-btn>
            </div>

            <div class="d-flex gap-1">
              <v-btn variant="tonal" @click="handleNextSong">
                Wrong answer
              </v-btn>
            </div>
          </div>
        </div>
      </div>
    </div>

    <v-dialog v-model="showTeamSettings" persistent style="width:500px;">
      <v-card>
        <v-card-text>
          Settings
        </v-card-text>

        <v-card-actions>
          <v-btn variant="text" @click="showTeamSettings=false">
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts" setup>
import 'animate.css';

import { ref } from 'vue';

const showTeamSettings = ref(false)
const scoreBoxEl = ref<HTMLElement>()

function handleAnswer () {
  if (scoreBoxEl.value) {
    const animationClasses = ['animate__animated', 'animate__heartBeat', 'animate__repeat-1']

    scoreBoxEl.value.classList.remove(...animationClasses)
    void scoreBoxEl.value.offsetWidth;
    scoreBoxEl.value.classList.add(...animationClasses)
  }
}

function handleNextSong () {
  // Do something
}

function handleIframeLoaded () {
  console.log('Iframe')
}
</script>

<style lang="scss" scoped>
%score {
  width: 100px;
  height: auto;
  min-height: 10px;
  text-align: center;
}

.blind-test {
  .teams {
    height: 100vh;
    width: 100%;
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr;

    .team {
      padding: 1rem;
    }
  
    .score {
      @extend %score;
    }
  }

  .video {
    position: absolute;
    top: 10%;
    min-width: 420px;
    height: auto;
    left: 34%;
  }
}
</style>
