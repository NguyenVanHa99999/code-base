import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// plugins
import { I18n, PrimeVuePlugin } from '@/plugins'

// styles
import '@/assets/scss/common.scss'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// plugins setting
app.use(I18n)
app.use(PrimeVuePlugin)
app.mount('#app')
