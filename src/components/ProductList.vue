<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardFooter,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface ProductProps {
  id: string;
  imageUrl: string;
  name: string;
  price: number;
  store: string;
  url: string;
}

const productList = ref<ProductProps[]>([]);
const route = useRoute();
const searchQuery = computed(() =>
  (route.query.q || '').toString().toLowerCase()
);

// Ambil data dari backend
onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/product');
    console.log('DATA DARI BACKEND:', response.data);

    productList.value = response.data.map((product: any) => ({
      id: product.id,
      imageUrl: product.imageUrl,
      name: product.name,
      store: product.store,
      url: product.url,
      price: parseInt(product.price.replace(/\D/g, '')) || 0,
    }));
  } catch (error) {
    console.error('Gagal memuat produk:', error);
  }
});

// Filter, acak, dan batasi 10 produk
const filteredProducts = computed(() => {
  const result = searchQuery.value
    ? productList.value.filter((product) =>
        product.name?.toLowerCase().includes(searchQuery.value)
      )
    : productList.value;

  const shuffled = [...result].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, 10);
});

// Format harga ke Rupiah
const formatPrice = (price: number) =>
  new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0,
  }).format(price);

const categories = [
  { name: 'Handphone', image: '/kategori/handphone.png' },
  { name: 'Headphone', image: '/kategori/headset.png' },
  { name: 'Kulkas', image: '/kategori/kulkas.png' },
  { name: 'Laptop', image: '/kategori/laptop.png' },
  { name: 'Speaker', image: '/kategori/speaker.png' },
];
</script>

<template>
  <section class="py-32 bg-white dark:bg-background">
    <div class="text-center mb-10">
      <h2 class="text-lg text-primary mb-2 tracking-wider">Produk Terbaik</h2>
      <h2 class="text-3xl md:text-4xl font-bold">Telusuri Harga Produk Terbaikmu</h2>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-2">
      <div
        v-for="category in categories"
        :key="category.name"
        class="flex flex-col items-center hover:scale-105 transition-transform duration-200"
      >
        <img
          :src="category.image"
          :alt="category.name"
          class="w-36 h-36 object-contain mb-2"
        />
        <span class="text-lg font-semibold">{{ category.name }}</span>
      </div>
    </div>
  </section>

  <section id="products" class="max-w-[80%] mx-auto py-12 sm:py-16">
    <div class="text-center mb-8">
      <h2 class="text-lg text-primary mb-2 tracking-wider">Produk Terbaik</h2>
      <h2 class="text-3xl md:text-4xl font-bold">Harga Elektronik Terbaik</h2>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-5">
      <Card
        v-for="product in filteredProducts"
        :key="product.id"
        class="bg-muted/60 dark:bg-card flex flex-col h-full overflow-hidden group/hoverimg hover:shadow-lg transition-shadow duration-200"
      >
        <CardHeader class="p-0 gap-0 relative">
          <div class="h-full overflow-hidden">
            <img
              :src="product.imageUrl"
              :alt="product.name"
              class="w-full aspect-square object-cover transition-all duration-200 ease-linear size-full group-hover/hoverimg:scale-[1.02]"
            />
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

        <CardFooter class="p-4 pt-0">
          <a :href="product.url" target="_blank" class="w-full">
            <Button class="w-full">Lihat di {{ product.store }}</Button>
          </a>
        </CardFooter>
      </Card>

      <!-- Tombol lihat semua -->
      <div class="mt-10 flex justify-center col-span-full">
        <router-link to="/product">
          <Button variant="outline">Lihat Semua Produk ></Button>
        </router-link>
      </div>
    </div>
  </section>
</template>
