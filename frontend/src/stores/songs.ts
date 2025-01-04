import { defineStore } from "pinia";
import { computed, ref } from "vue";
import type { Answer, CacheSession, Song } from "../types";
import defaults from '../data/defaults.json'

export const useSongs = defineStore('songs', () => {
    const cache = ref<CacheSession>(defaults.cache)

    const selectedSongs = ref<Song[]>([])

    const correctAnswers = ref<Answer[]>([])
    const incorrectAnswers = ref<Answer[]>([])

    const scoringTimelineBase = ref(100)
    const scoringTimeline = ref<number[]>([])

    const isStarted = ref(false)


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

    const currentSong = computed(() => {
        if (cache.value) {
            return cache.value.songs[cache.value.songs.length - 1]
        } else {
            return null
        }
    })    

    function updateScoringTimeline (action: 'add' | 'sub') {
        const lastScore = scoringTimeline.value[scoringTimeline.value.length]

        if (lastScore) {
            if (action === 'add') {
                scoringTimeline.value.push(lastScore + 1)
            } else {
                scoringTimeline.value.push(lastScore - 1)
            }
        } else {
            if (action === 'add') {
                scoringTimeline.value.push(100 + 1)
            }
            
            if (action === 'sub') {
                scoringTimeline.value.push(100 - 1)
            }
        }

    }

    return {
        cache,
        isStarted,
        updateScoringTimeline,
        scoringTimelineBase,
        scoringTimeline,
        firstTeamScore,
        secondTeamScore,
        correctAnswers,
        incorrectAnswers,
        currentSong,
        selectedSongs
    }
})
