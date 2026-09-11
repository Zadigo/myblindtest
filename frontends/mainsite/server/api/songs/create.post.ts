import { SongCreationApiResponse } from '#shared/types'

export default defineEventHandler(async (event) => {
  try {
    const cleanedData = await readBody(event)
    return await $fetch<SongCreationApiResponse>('/api/v1/songs/create', {
      method: 'post',
      baseURL: useRuntimeConfig().public.apiBaseUrl,
      body: cleanedData
    })
  } catch (error) {
    console.error(error)
  }
})
