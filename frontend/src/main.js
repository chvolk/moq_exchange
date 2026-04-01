import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import api from './services/api'  // Make sure this import is correct

const app = createApp(App)

app.use(router)
app.use(store)
app.use(vuetify)

// Provide the API instance
app.provide('api', api)

app.mount('#app')