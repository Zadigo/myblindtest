import type { Arrayable } from './utils'

export interface StatisticsData {
  labels: Arrayable<string | number>
  data: Arrayable<number>
}

export interface StatisticsApiResponse {
  distribution_by_genre: StatisticsData
}
