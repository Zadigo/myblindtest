import type { Arrayable } from '.'

export interface StatisticsData {
  labels: Arrayable<string | number>,
  data: Arrayable<number>
}

export interface StatisticsApiResponse {
  distribution_by_genre: StatisticsData
}
