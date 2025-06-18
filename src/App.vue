<template>
  <div>
    <Navbar v-if="!isAuthPage" />
    <router-view />  <!-- isi halaman berubah-ubah -->
    <Footer v-if="!isAuthPage" />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'

export default {
  components: {
    Navbar,
    Footer
  },
  computed: {
    isAuthPage() {
      // bisa disesuaikan kalau nanti ada /register juga
      return this.$route.path === '/login'
    }
  }
}
</script>



<!-- <script setup lang="ts">
import Navbar from "./components/Navbar.vue";
import Hero from "./components/Hero.vue";
import Benefits from "./components/Benefits.vue";
import Features from "./components/Features.vue";
import Services from "./components/Services.vue";
import HowItWorks from "./components/HowItWorks.vue";
import Sponsors from "./components/Sponsors.vue";
import Testimonials from "./components/Testimonials.vue";
import Product from "./components/Product.vue";
import Pricing from "./components/Pricing.vue";
import Community from "./components/Community.vue";
import Contact from "./components/Contact.vue";
import FAQ from "./components/FAQ.vue";
import Footer from "./components/Footer.vue";
import Login from "./components/Login.vue";
</script>

<template>
  <Navbar />
  <Hero />
  <Team />
  <Product />
  <Login />
  <Sponsors />
  <Benefits />
  <Features />
  <Services />
  <HowItWorks />
  <Testimonials />
  <Community />
  <Pricing />
  <Contact />
  <FAQ />
  <Footer />
</template> -->
