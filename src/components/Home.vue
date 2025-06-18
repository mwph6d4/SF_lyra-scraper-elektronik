<template>
    <div>
        <Hero />
        <ProductList />
        <!-- <Login /> -->
    </div>
</template>

<script setup>
import Hero from './Hero.vue'
import ProductList from './ProductList.vue'

import Swal from 'sweetalert2'
import { onMounted } from 'vue'

onMounted(() => {
  const justLoggedIn = sessionStorage.getItem('justLoggedIn')
  const username = localStorage.getItem('username')

  if (justLoggedIn && username) {
    Swal.fire({
      icon: "success",
      title: "Login Berhasil",
      text: `Haloo ${username}, Selamat datang !`,
      confirmButtonColor: "#22c55e", // kamu bisa sesuaikan warnanya
      timer: 2000,
    });

    // Hapus setelah ditampilkan
    sessionStorage.removeItem('justLoggedIn')
  }
})
</script>
