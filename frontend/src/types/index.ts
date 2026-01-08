import type { Ref } from 'vue'

export type * from './create'
export type * from './game'
export type * from './songs'
export type * from './vue'
export type * from './statistics'

export type Nullable<T> = T | null

export type Undefineable<T> = T | undefined

export type Empty<T> = Nullable<T> | Undefineable<T>

export type Refeable<T> = Ref<T>

export type Arrayable<T> = T[]

export type DefaultType<T, D> = T | D

export type PrimeVueToast =  ReturnType<typeof import('primevue/usetoast').useToast>

export type VueUseWsReturnType<T = unknown> = ReturnType<typeof import('@vueuse/core').useWebSocket<T>>

export type CastToString<T> = T extends object ? { [K in keyof T]: CastToString<T[K]> } : T extends Array<infer U> ? Array<CastToString<U>> : string

export type MultiDictType<T> = Record<string, T>

export interface BaseApiResponse<T> {
  next: number
  previous: number
  results: T[]
}

export interface _DatabaseItem {
  id: number
  created_on: string
}
