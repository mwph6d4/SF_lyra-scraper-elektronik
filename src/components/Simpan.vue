<script setup lang="ts">
import { onMounted, ref } from "vue";
import axios from "axios";
import Swal from "sweetalert2";
import "sweetalert2/dist/sweetalert2.min.css";

interface Produk {
  id: number;
  name: string;
  price: string;
  url: string;
  imageUrl: string;
  store: string;
}

const produkList = ref<Produk[]>([]);

const fetchSavedProducts = async () => {
  const userData = localStorage.getItem("user");
  const token = localStorage.getItem("token");

  if (!userData || !token) {
    console.error("User atau token tidak ditemukan di localStorage.");
    return;
  }

  const user = JSON.parse(userData);
  const user_id = user.id;

  try {
    const response = await axios.get("http://localhost:5000/api/saved-products", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      params: { user_id },
    });

    produkList.value = response.data;
  } catch (error) {
    console.error("Gagal memuat produk tersimpan:", error);
  }
};

const deleteProduct = async (produk_id: number) => {
  const result = await Swal.fire({
    title: "Hapus Produk?",
    text: "Apakah kamu yakin ingin menghapus produk ini dari favorit?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#d33",
    cancelButtonColor: "#3085d6",
    confirmButtonText: "Ya, hapus",
    cancelButtonText: "Batal",
  });

  if (!result.isConfirmed) return;

  const userData = localStorage.getItem("user");
  const token = localStorage.getItem("token");

  if (!userData || !token) {
    console.error("User atau token tidak ditemukan.");
    return;
  }

  const user = JSON.parse(userData);
  const user_id = user.id;

  try {
    await axios.delete("http://localhost:5000/api/delete-saved-product", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      data: { user_id, produk_id },
    });

    produkList.value = produkList.value.filter(p => p.id !== produk_id);

    Swal.fire("Dihapus!", "Produk berhasil dihapus dari favorit.", "success");
  } catch (error) {
    console.error("Gagal menghapus produk:", error);
    Swal.fire("Gagal", "Terjadi kesalahan saat menghapus produk.", "error");
  }
};

onMounted(fetchSavedProducts);
</script>

<template>
  <section id="saved-products" class="container md:w-[700px] py-24 sm:py-32">
    <div class="text-center mb-8">
      <h2 class="text-lg text-primary tracking-wider">Produk Disimpan</h2>
      <h2 class="text-3xl md:text-4xl font-bold">Produk Favoritmu</h2>
    </div>

    <div v-if="produkList.length === 0" class="text-center text-muted-foreground">
      Belum ada produk disimpan.
    </div>

    <div v-else class="grid gap-6">
      <div
        v-for="produk in produkList"
        :key="produk.id"
        class="border rounded-xl p-4 flex gap-4 items-center justify-between hover:shadow-md transition"
      >
        <div class="flex gap-4 items-center">
          <img
            :src="produk.imageUrl"
            alt="Gambar produk"
            class="w-24 h-24 object-cover rounded-lg"
          />
          <div>
            <a :href="produk.url" target="_blank" class="font-semibold text-lg hover:underline">
              {{ produk.name }}
            </a>
            <div class="text-muted-foreground mt-1">{{ produk.price }}</div>
            <div class="text-sm text-gray-500">Toko: {{ produk.store }}</div>
          </div>
        </div>
        <button
          @click="deleteProduct(produk.id)"
          class="bg-red-500 text-white rounded-full px-4 py-2 text-sm hover:bg-red-600 transition"
        >
          Hapus
        </button>
      </div>
    </div>
  </section>
</template>
