import type { Ref } from 'vue'

export type * from './create'
export type * from './game'
export type * from './messages'
export type * from './songs'
export type * from './vue'

export type Nullable<T> = T | null

export type Undefineable<T> = T | undefined

export type Refeable<T> = Ref<T>

export type Arrayable<T> = T[]

export interface BaseApiResponse<T> {
  next: number
  previous: number
  results: T[]
}
