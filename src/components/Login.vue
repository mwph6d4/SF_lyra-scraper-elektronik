<template>
  <div class="min-h-screen bg-gradient-to-br from-card to-muted/50 flex items-center justify-center px-4">
    <div class="flex flex-col md:flex-row items-center justify-center gap-8 max-w-6xl w-full">
      <!-- Logo -->
      <div class="flex justify-center md:justify-end w-full md:w-1/2 mr-32">
        <img
          src="@/assets/logo.png"
          alt="Selamat Datang"
          class="w-40 sm:w-60 md:w-80 lg:w-[28rem]"
        />
      </div>

      <!-- Form Login/Register -->
      <div class="w-full max-w-md bg-card rounded-xl shadow-lg overflow-hidden border">
        <!-- Tabs -->
      <div class="flex border-b">
        <button
          @click="() => { isLogin = true; resetForm(); }"
          :class="{
            'flex-1 py-4 px-6 font-medium text-center': true,
            'bg-primary/10 text-primary': isLogin,
            'hover:bg-muted/50': !isLogin
          }"
        >
          Login
        </button>
        <button
          @click="() => { isLogin = false; resetForm(); }"
          :class="{
            'flex-1 py-4 px-6 font-medium text-center': true,
            'bg-primary/10 text-primary': !isLogin,
            'hover:bg-muted/50': isLogin
          }"
        >
          Register
        </button>
      </div>

        <!-- Form Content -->
        <form @submit.prevent="isLogin ? handleLogin() : handleRegister()" class="p-6 space-y-6">
          <div class="space-y-2">
            <h2 class="text-2xl font-bold text-center">{{ isLogin ? 'Welcome Back!' : 'Create Account' }}</h2>
            <p class="text-muted-foreground text-center">
              {{ isLogin ? 'Login to access your account' : 'Register to start comparing prices' }}
            </p>
          </div>

          <div class="space-y-4">
            <!-- Username Field -->
            <div>
              <label for="username">Username</label>
              <input id="username" v-model="form.username" type="text" placeholder="Enter your username" class="w-full p-2 border rounded" required/>
            </div>

            <!-- Password Field -->
            <div>
              <label for="password">Password</label>
              <div class="relative">
                <input
                  id="password"
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="••••••••"
                  class="w-full p-2 border rounded pr-10"
                  required
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute right-2 top-1/2 transform -translate-y-1/2 text-sm text-gray-500"
                >
                  {{ showPassword ? 'Hide' : 'Show' }}
                </button>
              </div>
            </div>

            <!-- Confirm Password (Register only) -->
            <div v-if="!isLogin">
              <label for="confirmPassword">Confirm Password</label>
              <div class="relative">
                <input
                  id="confirmPassword"
                  v-model="form.confirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  placeholder="••••••••"
                  class="w-full p-2 border rounded pr-10"
                  required
                />
                <button
                  type="button"
                  @click="showConfirmPassword = !showConfirmPassword"
                  class="absolute right-2 top-1/2 transform -translate-y-1/2 text-sm text-gray-500"
                >
                  {{ showConfirmPassword ? 'Hide' : 'Show' }}
                </button>
              </div>
            </div>

            <!-- Error Message -->
            <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>

            <button type="submit" class="w-full bg-primary text-white py-2 rounded">
              {{ isLogin ? 'Login' : 'Register' }}
            </button>
          </div>

          <div class="text-center text-sm">
            {{ isLogin ? "Don't have an account?" : "Already have an account?" }}
            <button
              type="button"
              @click="isLogin = !isLogin"
              class="text-primary hover:underline"
            >
              {{ isLogin ? 'Register here' : 'Login here' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import Swal from "sweetalert2";
import { ref } from "vue";
import { useRouter } from "vue-router";
import { eventBus } from "@/EventBus";

const router = useRouter();
const isLogin = ref(true);
const error = ref("");

// Form data
const form = ref({
  username: "",
  password: "",
  confirmPassword: "" // Hanya untuk registrasi
});

const showPassword = ref(false);
const showConfirmPassword = ref(false);

// Fungsi untuk kosongkan field saat pindah form 
const resetForm = () => {
  form.value.username = "";
  form.value.password = "";
  form.value.confirmPassword = "";
  error.value = "";
};

// Fungsi Login
const handleLogin = async () => {
  error.value = "";
  try {
    const response = await fetch("http://localhost:5000/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: form.value.username,
        password: form.value.password
      })
    });

    const data = await response.json();

    if (response.status === 404) {
      Swal.fire({
        icon: "warning",
        title: "Username Tidak Ditemukan",
        text: "Silakan registrasi terlebih dahulu.",
        confirmButtonColor: "#a855f7",
      });
      isLogin.value = false;
      return;
    }

    if (response.ok && data.success) {
      // Simpan token dan user info
      localStorage.setItem("token", data.token);
      localStorage.setItem("user", JSON.stringify({ username: data.username, id: data.id }));
      sessionStorage.setItem("justLoggedIn", "true");
      eventBus.emit("user-logged-in");

      // ✅ Tampilkan Swal terlebih dahulu
      await Swal.fire({
        icon: "success",
        title: "Login Berhasil",
        text: `Selamat datang, ${data.username}!`,
        confirmButtonColor: "#22c55e"
      });

      // ✅ Ambil route tujuan
      const route = router.currentRoute.value;
      const redirect = route.query.redirect || "/home";
      const compare = route.query.compare;

      // ✅ Redirect setelah swal selesai
      router.push({
        path: redirect as string,
        query: compare ? { compare: compare as string } : {},
      });

    } else {
      error.value = data.message || "Login gagal!";
    }
  } catch (e) {
    console.error(e);
    error.value = "Gagal koneksi ke server";
  }
};


// Fungsi Register
const handleRegister = async () => {
  if (form.value.password !== form.value.confirmPassword) {
    error.value = "Password tidak cocok!";
    return;
  }

  const password = form.value.password;
  if (password.length < 8 || !/[A-Z]/.test(password) || !/\d/.test(password)) {
    error.value = "Password minimal harus 8 karakter, mengandung huruf besar dan angka!";
    return;
  }

  try {
    const response = await fetch("http://localhost:5000/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: form.value.username,
        password: password
      })
    });

    const data = await response.json();

    if (response.ok && data.success) {
      await Swal.fire({
        icon: "success",
        title: "Registrasi Berhasil",
        text: "Silakan login untuk melanjutkan.",
        confirmButtonColor: "#22c55e"
      });

      resetForm();      // ⬅️ Kosongkan field setelah sukses
      isLogin.value = true; // ⬅️ Beralih ke tab login
    } else {
      error.value = data.message || "Registrasi gagal!";
    }
  } catch (e) {
    console.error(e);
    error.value = "Gagal koneksi ke server";
  }
};


</script>
