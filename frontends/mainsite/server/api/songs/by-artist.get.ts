import type { ApiResponse, SongSearchParams } from "#shared/types"

export default defineEventHandler(async (event) => {
  try {
    const searchParam = getQuery<SongSearchParams>(event)
    return await $fetch<ApiResponse>('/api/v1/songs/by-artists', {
      method: 'GET',
      baseURL: useRuntimeConfig().public.apiBaseUrl,
      query: searchParam
    })
  } catch (error) {
    console.error(error)
  }
})
