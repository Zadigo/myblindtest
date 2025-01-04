<template>
  <section class="site">
    <BaseNavbar />
    <Toaster position="top-right" />

    <section class="container my-5">
      <div class="row">
        <div class="col-sm-12 col-md-12">
          <div class="card shadow-sm mb-2">
            <div class="card-body">
              <BaseTabs />
            </div>
          </div>
        </div>

        <div class="col-sm-12 col-md-6">
          <div class="card shadow-sm">
            <div class="card-body">
              <h1 v-if="currentSong" class="h4">
                {{ currentSong.name }}
              </h1>

              <h1 v-else class="h4">
                Loading...
              </h1>

              <div v-if="currentSong" class="fw-light d-flex gap-2 align-items-center">
                <p class="m-0">
                  {{ currentSong.artist }}
                </p>
                
                <div class="badge badge-success">
                  {{ currentSong.genre }}
                </div>
              </div>

              <div v-else class="fw-light">
                Loading...
              </div>

              <hr class="my-4">

              <div class="d-flex justify-content-end">
                <button :disabled="!isStarted" type="button" class="btn btn-light btn-rounded shadow-none" @click="handleNextSong">
                  <FontAwesomeIcon class="me-2" icon="close" /> Failed
                </button>

                <button :disabled="!isStarted" type="button" class="btn btn-primary btn-rounded shadow-none" @click="handleNextSong">
                  <FontAwesomeIcon class="me-2" icon="check" /> Success
                </button>
              </div>
            </div>
          </div>

          <div class="card shadow-sm mt-2">
            <div class="card-body d-flex gap-2">            
              <button v-if="isStarted" type="button" class="btn btn-danger btn-rounded shadow-none" @click="handleStop">
                <FontAwesomeIcon class="me-2" icon="stop" /> Stop
              </button>

              <button v-if="isStarted" type="button" class="btn btn-warning btn-rounded shadow-none" @click="handleStart">
                <FontAwesomeIcon class="me-2" icon="refresh" /> Reconnect
              </button>

              <button v-else type="button" class="btn btn-success btn-rounded shadow-none" @click="handleStart">
                Start
              </button>
            </div>
          </div>
        </div>

        <div class="col-sm-12 col-md-6">
          <div class="card shadow-sm mb-2">
            <div class="card-body">
              <p class="m-0 fw-bold">
                {{ sessionCache.currentStep }} song
              </p>
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
import { Toaster, toast } from 'vue-sonner'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { useWebSocket } from '@vueuse/core'
import { useHead } from 'unhead';
import { computed } from 'vue';
import type { SessionCache, Song } from '@/types';
import { useSessionStorage } from '@vueuse/core'

// import z from 'zod'

import BaseNavbar from './components/BaseNavbar.vue';
import BaseTabs from './components/BaseTabs.vue';

const sessionCache = useSessionStorage<SessionCache>('cache', { songs: [], currentStep: 0 }, {
  serializer: {
    read (raw) {
      return JSON.parse(raw)
    },
    write (value) {
      return JSON.stringify(value)
    },
  }
})

useHead({
  title: 'Blind test'
})

const ws = useWebSocket('ws://127.0.0.1:8000/ws/songs', {
  immediate: false,
  onConnected() {

  },
  onMessage() {
    const data = JSON.parse(ws.data.value)

    if (data.type === 'get.song') {
      // selectedSongs.value.push(data.data as Song)
      sessionCache.value.songs.push(data.data as Song)
    }
    
    if (data.type === 'next.song') {
      // const existingSong = selectedSongs.value.filter(x => x.id === data.data.id)
      const existingSong = sessionCache.value.songs.filter(x => x.id === data.data.id)
      if (existingSong.length > 0) {
        toast.error('Song already played')
      } else {
        sessionCache.value.songs.push(data.data as Song)
      }
    }
  },
  onDisconnected() {
    toast.error('Disconnected from a asgi', {

    })
  },
  onError() {

  }
})

const isStarted = computed(() => {
  return ws.status.value === 'OPEN'
})

const currentSong = computed(() => {
  return sessionCache.value.songs[sessionCache.value.songs.length - 1]
})

function sendMessage (data: Record<string, string | number[]>) {
  return JSON.stringify(data)
}

function handleStart () {
  ws.open()
  ws.send(sendMessage({ type: 'get.song' }))
  toast.success('Started blind test')
}

function handleStop () {
  ws.close()
  toast.success('Stopped blind test')
  sessionCache.value.songs = []
  sessionCache.value.currentStep = 0
}

function handleNextSong () {
  sessionCache.value.currentStep += 1
  ws.send(sendMessage({ type: 'next.song', exclude: sessionCache.value.songs.map(x => x.id) }))
}
</script>
