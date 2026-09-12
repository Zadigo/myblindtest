import { createErrorTemplate } from '#shared/errors'

export default defineEventHandler(async (event) => {
  try {
    const { docRef } = await getOrCreateSession(event)
    return { sessionId: docRef.id } as SessionApiResponse
  } catch (error) {
    console.error('Error creating session:', error)
    const template = createErrorTemplate(error)
    throw createError(template)
  }
})
