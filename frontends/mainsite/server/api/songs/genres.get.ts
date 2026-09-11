import { SearchedGenreApiResponse } from "#shared/types"

export default defineEventHandler(async (_event) => {
  try {
    return await $fetch<SearchedGenreApiResponse>('/api/v1/songs/genres', {
      method: 'GET',
      baseURL: useRuntimeConfig().public.apiBaseUrl
    })
  } catch (error) {
    console.error(error)
  }
})
