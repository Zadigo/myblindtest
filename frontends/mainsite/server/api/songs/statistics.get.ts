export default defineEventHandler(async (_event) => {
  try {
    return await $fetch<StatisticsApiResponse>('/api/v1/songs/statistics', {
      method: 'get',
      baseURL: useRuntimeConfig().public.apiBaseUrl
    })
  } catch (error) {
    console.error(error)
  }
})
