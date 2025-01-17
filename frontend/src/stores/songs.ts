import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { defaults } from '../data/defaults';
import type { Answer, CacheSession } from "../types";

export const useSongs = defineStore('songs', () => {
    const cache = ref<CacheSession>(defaults.cache)

    const correctAnswers = ref<Answer[]>([])

    const scoringTimelineBase = ref(100)
    const scoringTimeline = ref<number[]>([])

    const gameStarted = ref(false)

    const firstTeamScore = computed(() => {
        if (cache.value) {
            return cache.value.teams[0].score
        } else {
            return 0
        }
    })

    const secondTeamScore = computed(() => {
        if (cache.value) {
            return cache.value.teams[1].score
        } else {
            return 0
        }
    })

    // Returns the currect song on which the 
    // players will be trying to guess
    const currentSong = computed(() => {
        if (cache.value) {
            return cache.value.songs[cache.value.songs.length - 1]
        } else {
            return null
        }
    })

    return {
        cache,
        gameStarted,
        scoringTimelineBase,
        scoringTimeline,
        firstTeamScore,
        secondTeamScore,
        correctAnswers,
        currentSong
    }
})
