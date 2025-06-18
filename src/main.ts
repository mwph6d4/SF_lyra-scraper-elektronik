import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // Pastikan file router ada di src/router/index.js
import './assets/index.css'

// Buat aplikasi Vue terlebih dahulu
const app = createApp(App)

// Gunakan router sebelum mounting
app.use(router)

// Mount aplikasi
app.mount('#app')

// createApp(App).use(router).mount('#app')