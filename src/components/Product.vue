<script setup lang="ts">
// ===========================
// Imports
// ===========================
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router'; 
import { useColorMode } from "@vueuse/core";
import axios from 'axios';
import Swal from "sweetalert2";
import {
  Card, CardContent, CardHeader, CardTitle, CardFooter,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

// ===========================
// Setup & State
// ===========================
useColorMode();
const route = useRoute();
const router = useRouter();

interface ProductProps {
  id: string;
  imageUrl: string;
  name: string;
  price: number;
  store: string;
  url: string;
  brand: string;
  category: string;
}

const productList = ref<ProductProps[]>([]);
const savedProducts = ref<string[]>([]);
const compareList = ref<ProductProps[]>([]);
const showCompareResult = ref(false);

// Filter state
const selectedCategory = ref('Semua');
const selectedBrand = ref('Semua');
const minPrice = ref(0);
const maxPrice = ref(20000000);
const sortOrder = ref('termurah');

// ===========================
// Computed
// ===========================
const categoryOptions = computed(() => {
  const categories = new Set(productList.value.map(p => p.category));
  return ['Semua', ...Array.from(categories)];
});

const brandOptions = computed(() => {
  const brands = new Set(productList.value.map(p => p.brand));
  return ['Semua', ...Array.from(brands)];
});

const filteredProducts = computed(() => {
  let products = [...productList.value];
  const isFiltered = searchQuery.value || selectedCategory.value !== 'Semua' || minPrice.value !== 0 || maxPrice.value !== 20000000;

  if (searchQuery.value) {
    products = products.filter(product => product.name?.toLowerCase().includes(searchQuery.value));
  }
  if (selectedCategory.value !== 'Semua') {
    products = products.filter(p => p.category === selectedCategory.value);
  }
  if (selectedBrand.value !== 'Semua') {
    products = products.filter(p => p.brand === selectedBrand.value);
  }

  products = products.filter(p => p.price >= minPrice.value && p.price <= maxPrice.value);
  products.sort((a, b) => sortOrder.value === 'termurah' ? a.price - b.price : b.price - a.price);

  return !isFiltered ? shuffleArray(products).slice(0, 50) : products;
});

const bestProduct = computed(() => {
  if (!compareList.value.length) return null;
  return compareList.value.reduce((best, current) => current.price < best.price ? current : best, compareList.value[0]);
});

const searchQuery = computed(() => (route.query.q || "").toString().toLowerCase());
const kategoriQuery = computed(() => route.query.kategori?.toString() || 'Semua');

// ===========================
// Lifecycle & Initialization
// ===========================
onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/product');
    productList.value = response.data.map((product: any) => {
      const name = product.name || "";
      const brand = name.split(" ")[0];
      return {
        id: product.id,
        imageUrl: product.imageUrl,
        name: product.name,
        store: product.store,
        url: product.url,
        price: parseInt(product.price.replace(/\D/g, '')) || 0,
        brand: brand,
        category: product.category || 'Lainnya',
      };
    });

    const productIdToCompare = route.query.compare?.toString();
    if (productIdToCompare) {
      const productToAdd = productList.value.find(p => p.id === productIdToCompare);
      if (productToAdd && !compareList.value.some(p => p.id === productIdToCompare)) {
        compareList.value.push(productToAdd);
      }
      router.replace({ path: route.path, query: { ...route.query, compare: undefined } });
    }

    const kategoriURL = route.query.kategori?.toString();
    if (kategoriURL && categoryOptions.value.includes(kategoriURL)) {
      selectedCategory.value = kategoriURL;
    }
  } catch (error) {
    console.error("Gagal memuat data:", error);
  }
});

watch(kategoriQuery, (val) => {
  selectedCategory.value = val && categoryOptions.value.includes(val) ? val : 'Semua';
});

watch(() => route.query.kategori, (kategoriBaru) => {
  selectedCategory.value = kategoriBaru && typeof kategoriBaru === "string" && categoryOptions.value.includes(kategoriBaru) ? kategoriBaru : "Semua";
}, { immediate: true });

// ===========================
// Methods
// ===========================
const getUser = () => {
  const raw = localStorage.getItem('user');
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
};

const saveProduct = async (product: ProductProps) => {
  const user = getUser();
  if (!user || !user.id) {
    Swal.fire({ icon: "warning", title: "Login Diperlukan", text: "Silakan login untuk menyimpan produk.", confirmButtonColor: "#a855f7" });
    return;
  }

  try {
    await axios.post('http://localhost:5000/api/save-product', { user_id: user.id, product });
    savedProducts.value.push(product.id);
    Swal.fire({ icon: "success", title: "Produk Berhasil Disimpan!", text: `Produk \"${product.name}\" telah disimpan ke daftar favorit kamu.`, confirmButtonColor: "#a855f7" });
  } catch (error) {
    console.error("Gagal menyimpan produk:", error);
    Swal.fire({ icon: "error", title: "Gagal Menyimpan", text: "Terjadi kesalahan saat menyimpan produk. Coba lagi nanti.", confirmButtonColor: "#ef4444" });
  }
};

const toggleCompare = (product: ProductProps) => {
  const user = getUser();
  if (!user || !user.id) {
    Swal.fire({ icon: "warning", title: "Login Diperlukan", text: "Silakan login untuk menggunakan fitur perbandingan.", confirmButtonColor: "#a855f7" })
      .then(() => router.push({ path: "/login", query: { redirect: "/product", compare: product.id } }));
    return;
  }

  const index = compareList.value.findIndex(p => p.id === product.id);
  if (index !== -1) {
    compareList.value.splice(index, 1);
  } else {
    if (compareList.value.length >= 3) {
      Swal.fire({ icon: "warning", title: "Maksimal 3 produk", text: "Kamu hanya bisa membandingkan hingga 3 produk." });
      return;
    }
    compareList.value.push(product);
  }
};

const openCompareResult = () => {
  const user = getUser();
  if (!user || !user.id) {
    Swal.fire({ icon: "warning", title: "Login Diperlukan", text: "Silakan login untuk melihat hasil perbandingan.", confirmButtonColor: "#a855f7" })
      .then(() => router.push({ path: "/login", query: { redirect: "/product" } }));
    return;
  }

  if (compareList.value.length < 2) {
    alert("Pilih minimal 2 produk untuk dibandingkan.");
    return;
  }
  showCompareResult.value = true;
};

// ===========================
// Utils
// ===========================
const isSaved = (id: string) => savedProducts.value.includes(id);
const isCompared = (id: string) => compareList.value.some(p => p.id === id);

const formatPrice = (price: number) =>
  new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0
  }).format(price);

function shuffleArray<T>(array: T[]): T[] {
  return array
    .map(value => ({ value, sort: Math.random() }))
    .sort((a, b) => a.sort - b.sort)
    .map(({ value }) => value);
}
</script>


<template>
  <!-- Daftar Produk -->
  <section id="products" class="max-w-[90%] mx-auto py-12 sm:py-16">
    <div class="text-center mb-8">
      <h2 class="text-lg text-primary mb-2 tracking-wider">Produk Terbaik</h2>
      <h2 class="text-3xl md:text-4xl font-bold">Harga Elektronik Terbaik</h2>
    </div>

    <!-- Filter user -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end mb-8">  
      <!-- Kategori Dropdown -->
      <div class="w-full">
        <label class="block mb-1 font-semibold">Kategori</label>
        <select v-model="selectedCategory" class="w-full border rounded p-2">
          <option v-for="option in categoryOptions" :key="option" :value="option">
            {{ option }}
          </option>
        </select>
      </div>

      <!-- Brand Dropdown -->
      <div class="w-full">
        <label class="block mb-1 font-semibold">Brand</label>
        <select v-model="selectedBrand" class="w-full border rounded p-2">
          <option v-for="brand in brandOptions" :key="brand" :value="brand">
            {{ brand }}
          </option>
        </select>
      </div>

      <!-- Range Harga -->
      <div class="w-full">
        <label class="block mb-1 font-semibold">Harga (Rp)</label>
        <div class="flex items-center gap-2">
          <input type="number" v-model.number="minPrice" class="border rounded w-full p-2" placeholder="Min" />
          <span>-</span>
          <input type="number" v-model.number="maxPrice" class="border rounded w-full p-2" placeholder="Max" />
        </div>
      </div>

      <!-- Urutkan Harga -->
      <div class="w-full">
        <label class="block mb-1 font-semibold">Urutkan</label>
        <select v-model="sortOrder" class="w-full border rounded p-2">
          <option value="termurah">Harga Termurah</option>
          <option value="termahal">Harga Termahal</option>
        </select>
      </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-5">
      <!-- Produk Tidak Tersedia -->
      <div v-if="filteredProducts.length === 0" class="text-center col-span-full text-gray-500 text-lg mt-10">
        Produk tidak tersedia untuk filter yang dipilih.
      </div>

      <Card
        v-for="product in filteredProducts"
        :key="product.id"
        class="bg-muted/60 dark:bg-card flex flex-col h-full overflow-hidden group/hoverimg hover:shadow-lg transition-shadow duration-200">
        <CardHeader class="p-0 gap-0 relative">
          <div class="h-full overflow-hidden">
            <img
              :src="product.imageUrl"
              :alt="product.name"
              class="w-full aspect-square object-cover transition-all duration-200 ease-linear size-full group-hover/hoverimg:scale-[1.02]"/>
          </div>
        </CardHeader>

        <CardContent class="flex-1 p-4">
          <CardTitle class="text-lg mb-2 line-clamp-2">
            {{ product.name }}
          </CardTitle>
          <div class="mb-2">
            <span class="text-xl font-bold text-primary">
              {{ formatPrice(product.price) }}
            </span>
          </div>
        </CardContent>
        <CardFooter class="p-4 pt-0 flex flex-col gap-2">
          <Button
            variant="outline"
            class="w-full"
            @click="saveProduct(product)"
            :disabled="isSaved(product.id)">
            {{ isSaved(product.id) ? 'Tersimpan' : 'Simpan Produk' }}
          </Button>
          <Button
            variant="outline"
            class="w-full"
            @click="toggleCompare(product)">
            {{ isCompared(product.id) ? 'Hapus dari Compare' : 'Bandingkan' }}
          </Button>
          <a :href="product.url" target="_blank" class="w-full">
            <Button class="w-full">Lihat di {{ product.store }}</Button>
          </a>
        </CardFooter>
      </Card>
    </div>
  </section>

  <!-- Floating Compare Panel -->
  <Teleport to="body">
    <div
      v-if="showCompareResult"
      class="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4"
    >
      <div class="bg-white dark:bg-background rounded-xl w-full max-w-5xl p-6 overflow-auto max-h-[90vh] relative">
        <button class="absolute top-4 right-4 text-xl" @click="showCompareResult = false">✕</button>
        <h2 class="text-2xl font-bold mb-4 text-center">Hasil Perbandingan</h2>

        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          <Card
            v-for="product in compareList"
            :key="product.id"
            :class="[
              'border',
              bestProduct?.id === product.id ? 'border-green-600' : 'border-muted'
            ]"
            class="bg-white dark:bg-card"
          >
            <CardHeader>
              <img :src="product.imageUrl" alt="" class="w-full aspect-square object-cover rounded" />
            </CardHeader>
            <CardContent class="p-4 space-y-2">
              <CardTitle class="text-lg font-bold">{{ product.name }}</CardTitle>
              <p class="text-primary font-semibold text-xl">{{ formatPrice(product.price) }}</p>
              <p class="text-sm text-muted-foreground">Merek: {{ product.brand }}</p>
              <p class="text-sm text-muted-foreground">Toko: {{ product.store }}</p>
            </CardContent>
            <CardFooter class="p-4 pt-0">
              <a :href="product.url" target="_blank">
                <Button size="sm">Lihat Produk</Button>
              </a>
            </CardFooter>
          </Card>
        </div>

        <p class="mt-4 text-center text-green-600 font-semibold" v-if="bestProduct">
          Produk terbaik berdasarkan harga: <strong>{{ bestProduct.name }}</strong>
        </p>
      </div>
    </div>
  </Teleport>
    <!-- Tombol Compare Mengambang di Kanan Bawah -->
<!-- Tombol Compare Kotak di Kanan Bawah -->
<Teleport to="body">
  <div
    v-if="compareList.length > 0"
    class="fixed bottom-6 right-6 z-50 w-80 bg-white dark:bg-card border rounded-lg shadow-lg"
  >
    <!-- Header Toggle -->
    <div class="flex items-center justify-between px-4 py-2 border-b bg-primary text-white rounded-t-lg">
      <span class="font-semibold">Daftar Perbandingan</span>
      <button @click="compareList = []" title="Kosongkan daftar">
        ✕
      </button>
    </div>

    <!-- List Produk Terpilih -->
    <ul class="max-h-60 overflow-auto divide-y">
      <li
        v-for="product in compareList"
        :key="product.id"
        class="flex items-center justify-between gap-2 px-4 py-2"
      >
        <div class="flex items-center gap-2">
          <img :src="product.imageUrl" alt="Gambar" class="w-10 h-10 rounded object-cover" />
          <span class="text-sm line-clamp-1 max-w-[150px]">{{ product.name }}</span>
        </div>
        <button @click="toggleCompare(product)" class="text-gray-500 hover:text-red-600 text-lg">×</button>
      </li>
    </ul>

    <!-- Tombol Bandingkan -->
    <div class="p-3 border-t">
      <Button
        class="w-full"
        :disabled="compareList.length < 2"
        @click="openCompareResult"
      >
        Bandingkan ({{ compareList.length }})
      </Button>
    </div>
  </div>
</Teleport>
</template>
