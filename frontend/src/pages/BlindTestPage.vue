<template>
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

        <div class="d-flex justify-content-around gap-1">
          <ActionBlock :team-id="1" @next-song="handleNextSong" />
          <ActionBlock :team-id="2" @next-song="handleNextSong" />
        </div>
      </div>

      <div class="card-body">
        <div class="d-flex justify-content-center gap-2">
          <button type="button" class="btn btn-dark btn-rounded shadow-none">
            <FontAwesomeIcon icon="close" /> Wrong answer
          </button>

          <button v-if="isStarted" type="button" class="btn btn-danger btn-rounded shadow-none" @click="handleStop">
            <FontAwesomeIcon class="me-2" icon="stop" /> Stop
          </button>

          <button v-if="isStarted" type="button" class="btn btn-warning btn-rounded shadow-none" @click="handleStart">
            <FontAwesomeIcon class="me-2" icon="refresh" /> Reconnect
          </button>

          <button v-else type="button" class="btn btn-dark btn-rounded shadow-none" @click="handleStart">
            Start
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import ActionBlock from '@/components/blindtest/ActionBlock.vue';
import { useSongs } from '@/stores/songs';
import type { Song } from '@/types';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { useWebSocket } from '@vueuse/core';
import { storeToRefs } from 'pinia';
import { useHead } from 'unhead';
import { provide } from 'vue';
import { toast } from 'vue-sonner';

// import z from 'zod'

useHead({
  title: 'Blind test'
})

const songsStore = useSongs()
const { selectedSongs, currentSong, correctAnswers, incorrectAnswers, isStarted } = storeToRefs(songsStore)

const ws = useWebSocket('ws://127.0.0.1:8000/ws/songs', {
  immediate: false,
  onConnected() {
    songsStore.isStarted = true
  },
  onMessage() {
    const data = JSON.parse(ws.data.value)

    if (data.type === 'get.song') {
      if (songsStore.cache) {
        songsStore.cache.songs.push(data.data as Song)
      }
    }
    
    if (data.type === 'next.song') {
      if (songsStore.cache) {
        const existingSong = songsStore.cache.songs.filter(x => x.id === data.data.id)

        if (existingSong.length > 0) {
          toast.error('Song already played')
        } else {
          songsStore.cache.songs.push(data.data as Song)
        }
      }
    }
  },
  onDisconnected() {
    songsStore.isStarted = false
    toast.error('Disconnected from a asgi')
  },
  onError() {

  }
})

provide('isStarted', songsStore.isStarted)

function sendMessage (data: Record<string, string | number[] | boolean>) {
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

  if (songsStore.cache) {
    selectedSongs.value = []
    songsStore.cache.songs = []
    songsStore.cache.teams.forEach(x => {
      x.score = 0
    })
    songsStore.cache.currentStep = 0
  }
}

function handleNextSong (data: (number | boolean)[]) {
  const teamId = data[0]
  const correctAnswser = data[1]

  console.log(teamId, correctAnswser)

  if (songsStore.cache) {
    songsStore.cache.currentStep += 1

    if (correctAnswser && currentSong.value) {
      correctAnswers.value.push({
        song: currentSong.value
      })
    } 
    
    if (!correctAnswser && currentSong.value) {
      incorrectAnswers.value.push({
        song: currentSong.value
      })
    }

    ws.send(sendMessage({ 
      type: 'next.song', 
      exclude: songsStore.cache.songs.map(x => x.id)
    }))
  }
}
</script>
