import { createErrorTemplate } from '#shared/errors'

export default defineEventHandler(async (event) => {
  try {
    const body = await readBody<CacheSession>(event)
    const { docRef } = await getOrCreateSession(event)
    await docRef.update({...body, updatedAt: new Date()})

    return {
      state: 'Session updated successfully',
    }
  } catch (error) {
    const template = createErrorTemplate(error)
    throw createError(template)
  }
})
