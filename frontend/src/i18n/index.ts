import { createI18n } from 'vue-i18n'
import { messagesEn } from './locales/en-Us'
import { messagesFr } from './locales/fr-Fr'

export const SUPPORT_LOCALES = ['en-US', 'fr-FR']

export const _SUPPORT_LOCALES = ['en-US', 'fr-FR'] as const

export type LocalTypes = typeof _SUPPORT_LOCALES[number]

export const i18n = createI18n({
  legacy: false,
  globalInjection: true,
  locale: 'fr-FR',
  fallbackLocale: 'en-US',
  fallbackFormat: 'en-US',
  messages: {
    'fr-FR':  messagesFr,
    'en-US': messagesEn
  }

})

// export function useI18n() {
//   async function loadLocale(locale: LocalTypes) {
//     const messages = await import(/* webpackChunkName: "locale-[request]" */ `./locales/${locale}.ts`)
//     i18n.global.setLocaleMessage(locale, messages.default)
//     // return nextTick()
//   }

//   async function hasLocale(locale: LocalTypes) {
//     return i18n.global.availableLocales.includes(locale)
//   }

//   return {
//     hasLocale,
//     loadLocale
//   }
// }
