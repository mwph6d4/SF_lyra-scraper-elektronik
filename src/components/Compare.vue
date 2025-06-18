<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import {
  Card, CardContent, CardHeader, CardTitle, CardFooter,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface ProductProps {
  id: string;
  imageUrl: string;
  name: string;
  price: number;
  store: string;
  url: string;
}

const route = useRoute();
const compareList = ref<ProductProps[]>([]);

const formatPrice = (price: number) =>
  new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0
  }).format(price);

onMounted(async () => {
  const ids = (route.query.ids as string)?.split(',') || [];
  try {
    const response = await axios.get('http://localhost:5000/api/product');
    const allProducts = response.data.map((product: any) => ({
      id: product.id,
      imageUrl: product.imageUrl,
      name: product.name,
      store: product.store,
      url: product.url,
      price: parseInt(product.price.replace(/\D/g, '')) || 0,
    }));
    compareList.value = allProducts.filter((p: ProductProps) => ids.includes(p.id));
  } catch (error) {
    console.error("Gagal memuat data untuk perbandingan:", error);
  }
});
</script>

<template>
  <section class="py-32 bg-white dark:bg-background max-w-[90%] mx-auto">
    <div class="text-center mb-10">
      <h2 class="text-lg text-primary mb-2 tracking-wider">Bandingkan Produk</h2>
      <h2 class="text-3xl md:text-4xl font-bold">Perbandingan Produk Elektronik</h2>
    </div>

    <div v-if="compareList.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
      <Card v-for="product in compareList" :key="product.id" class="border border-primary/30 bg-white dark:bg-card">
        <CardHeader>
          <img :src="product.imageUrl" alt="" class="w-full aspect-square object-cover rounded" />
        </CardHeader>
        <CardContent class="p-4 space-y-2">
          <CardTitle class="text-lg font-bold">{{ product.name }}</CardTitle>
          <p class="text-primary font-semibold text-xl">{{ formatPrice(product.price) }}</p>
          <p class="text-sm text-muted-foreground">Toko: {{ product.store }}</p>
        </CardContent>
        <CardFooter class="p-4 pt-0">
          <a :href="product.url" target="_blank">
            <Button size="sm">Lihat Produk</Button>
          </a>
        </CardFooter>
      </Card>
    </div>

    <div v-else class="text-center mt-10">
      <p class="text-muted-foreground text-lg">Tidak ada produk untuk dibandingkan.</p>
    </div>
  </section>
</template>
