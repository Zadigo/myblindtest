import { createErrorTemplate } from '#shared/errors'

export default defineEventHandler(async (event) => {
  try {
    const { docRef } = await getOrCreateSession(event)
    const result = await docRef.get()
    return result.data() as CacheSession
  } catch(error) {
    const template = createErrorTemplate(error)
    throw createError(template)
  }
})
