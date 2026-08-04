export function useHTMLLangAttribute() {
  if (import.meta.client) {
    const { locale } = useI18n()

    async function create(value?: ReturnType<typeof useI18n>[ 'locale' ][ 'value' ]) {
      const langAttribute = document.createAttribute('lang')
      langAttribute.value = value || locale.value
      document.querySelector('html')?.setAttributeNode(langAttribute)
    }

    watchDebounced(locale, async (newLocale) => {
      await create(newLocale)
    }, { debounce: 300 })

    onMounted(async () => {
      await create()
    })
  }
}
