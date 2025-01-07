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
    youtube_id: '',
    year: 0,
    difficulty: 1
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
            matchSongDifficulty: false,
            difficultyLevel: 'All' as 'All' | 'Easy' | 'Medium' | 'Difficult' | 'Expert',
            songType: 'All' as 'All' | 'Pop' | 'Electro' | 'Rock'
        }
    }
}

export const wheelDetaults = [
    { id: 1, value: 'Pop', bgColor: '#7d7db3', color: '#ffffff' },
    { id: 2, value: 'Rock', bgColor: '#ffffff', color: '#000000' },
    { id: 3, value: 'Rythme and blues', bgColor: '#7d7db3', color: '#000000' },
    { id: 4, value: 'Rap', bgColor: '#ffffff', color: '#000000' },
    { id: 5, value: 'Blues', bgColor: '#7d7db3', color: '#000000' },
    { id: 6, value: 'Jazz', bgColor: '#ffffff', color: '#000000' },
    { id: 7, value: 'Indie', bgColor: '#7d7db3', color: '#000000' },
    { id: 8, value: 'Classical', bgColor: '#ffffff', color: '#000000' },
    { id: 9, value: 'Electro', bgColor: '#ffffff', color: '#000000' },
]
