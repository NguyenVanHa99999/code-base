import PrimeVue from 'primevue/config'
import { FoxgoTheme } from '@/theme/foxgo'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'


export const PrimeVuePlugin = {
  install: (app) => {
    app.use(PrimeVue, {
      theme: {
        preset: FoxgoTheme,
        options: {
          prefix: 'p',
          darkModeSelector: false || 'none',
          cssLayer: false
        }
      }
    })
    app.component('VButton', Button)
    app.component('VInput', InputText)
  }
}

export default PrimeVuePlugin
