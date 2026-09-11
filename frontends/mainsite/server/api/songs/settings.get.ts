export default defineEventHandler(async (_event) => {
  try {
    return await $fetch<SettingsApiResponse>('/api/v1/songs/settings', { 
      method: 'GET',
      baseURL: useRuntimeConfig().public.apiBaseUrl
    })
  } catch (error) {
    console.error(error)
  }
})
