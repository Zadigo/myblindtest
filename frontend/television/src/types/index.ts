export type * from './game'
export type * from './messages'
export type * from './session'
export type * from './songs'

export type Nullable<T> = T | null

export type Undefinedable<T> = T | undefined

export type PrimeVueToast = ReturnType<typeof import('primevue/usetoast').useToast>
