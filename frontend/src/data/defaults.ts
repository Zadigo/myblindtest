import type { CacheSession } from "../types";

export const difficultyLevels = [
    'All',
    'Easy',
    'Medium',
    'Difficult',
    'Expert'
]

export const songTypes = [
    'All',
    'Pop',
    'Electro',
    'Rock'
]

export const addNewSongData = {
    name: '',
    genre: '',
    artist: '',
    youtube: '',
    year: 0
}

export const defaults: { cache: CacheSession } = {
    cache: {
        songs: [],
        currentStep: 0,
        teams: [
            {
                name: '',
                score: 0,
                players: [],
                color: null
            },
            {
                name: '',
                score: 0,
                players: [],
                color: null
            }
        ],
        settings: {
            rounds: 1,
            timeLimit: 0,
            pointValue: 1,
            matchDifficulty: false,
            difficultyLevel: 'All' as 'All' | 'Easy' | 'Medium' | 'Difficult' | 'Expert',
            songType: 'All' as 'All' | 'Pop' | 'Electro' | 'Rock'
        }
    }
}
