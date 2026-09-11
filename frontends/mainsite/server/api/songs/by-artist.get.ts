import { ApiResponse } from "#shared/types"

export default defineEventHandler(async (event) => {
  try {
    const searchParam = getQuery(event)
    return await $fetch<ApiResponse>('/v1/songs/by-artists', {
      method: 'GET',
      baseURL: useRuntimeConfig().public.apiBaseUrl,
      query: searchParam
    })
  } catch (error) {
    console.error(error)
  }
})
