import { createI18n } from 'vue-i18n'

export const I18n = {
  instance: null,
}
const loadLocaleMessages = () => {
  const locales = import.meta.glob('../locales/*.json', { eager: true })
  const messages = {}
  Object.keys(locales).forEach((key) => {
    const matched = key.match(/([A-Za-z0-9-_]+)\.json$/i)
    if (matched && matched.length > 1) {
      const locale = matched[1]
      messages[locale] = locales[key].default
    }
  })
  return messages
}

I18n.install = (app) => {
  const i18n = createI18n({
    legacy: false,
    locale: import.meta.env.VITE_I18N_LOCALE || 'vi',
    fallbackLocale: import.meta.env.VITE_I18N_FALLBACK_LOCALE || 'vi',
    messages: loadLocaleMessages(),
  })

  I18n.instance = i18n

  app.use(i18n)
}

export default I18n
