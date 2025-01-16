import { defineStore } from "pinia"
import { ref } from "vue"

export const useSongs = defineStore('songs', () => {
    const buzzCounter = ref<number>(0)

    return {
        buzzCounter
    }
})
