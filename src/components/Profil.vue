<script setup lang="ts">
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { ref, onMounted, watch } from "vue";
import axios from "axios";
import Swal from "sweetalert2";

// State
const username = ref<string | null>(null);
const editedUsername = ref<string>("");
const showEditForm = ref<boolean>(false);
const message = ref<string | null>(null);
const error = ref<string | null>(null);

interface Product {
  name: string;
  price: string;
  url: string;
  imageUrl: string;
}

const userProducts = ref<Product[]>([]);

interface ProfilProps {
  question: string;
  answer: string;
  value: string;
}

const ProfilList = ref<ProfilProps[]>([
  {
    question: "Nama Pengguna / Username",
    answer: "",
    value: "item-1",
  },
  {
    question: "Produk Disimpan",
    answer: "",
    value: "item-2",
  },
]);

const updateProfilList = () => {
  const usernameIndex = ProfilList.value.findIndex((item) => item.value === "item-1");
  if (usernameIndex !== -1) {
    ProfilList.value[usernameIndex].answer = username.value || "Belum login";
  }

  const produkIndex = ProfilList.value.findIndex((item) => item.value === "item-2");
  if (produkIndex !== -1) {
    ProfilList.value[produkIndex].answer = `${userProducts.value.length} produk disimpan`;
  }
};

// Auto update saat username berubah
watch(username, updateProfilList);
watch(userProducts, updateProfilList);

const fetchUserProducts = async () => {
  const token = localStorage.getItem("token");
  const userId = localStorage.getItem("user_id");
  if (!token || !userId) return;

  try {
    const response = await axios.get(
      `http://localhost:5000/api/saved-products?user_id=${userId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    userProducts.value = response.data;
  } catch (error) {
    console.error("Gagal mengambil produk:", error);
  }
};

const deleteProduct = async (url: string) => {
  const token = localStorage.getItem("token");
  if (!token || !username.value) return;

  const confirm = await Swal.fire({
    title: "Hapus produk ini?",
    text: "Tindakan ini tidak bisa dibatalkan.",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Ya, hapus",
    cancelButtonText: "Batal",
  });

  if (!confirm.isConfirmed) return;

  try {
    await axios.post(
      "http://localhost:5000/api/products/delete",
      { link: url },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    userProducts.value = userProducts.value.filter(p => p.url !== url);
    Swal.fire("Berhasil", "Produk berhasil dihapus.", "success");
  } catch (err) {
    Swal.fire("Gagal", "Tidak dapat menghapus produk.", "error");
  }
};

onMounted(() => {
  const storedUser = localStorage.getItem("user");
  if (storedUser) {
    try {
      const parsedUser = JSON.parse(storedUser);
      if (parsedUser?.username) {
        username.value = parsedUser.username;
        editedUsername.value = parsedUser.username;
      } else {
        console.warn("Username tidak ditemukan di localStorage.");
      }
    } catch (err) {
      console.error("Gagal parse user:", err);
    }
  }
  fetchUserProducts();
});

const saveUsername = async (): Promise<void> => {
  error.value = null;
  message.value = null;
  const token = localStorage.getItem("token");
  if (!token) {
    error.value = "Token tidak ditemukan. Silakan login kembali.";
    return;
  }

  try {
    await axios.post(
      "http://localhost:5000/api/user/update",
      {
        old_username: username.value,
        new_username: editedUsername.value,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    username.value = editedUsername.value;

    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      try {
        const parsedUser = JSON.parse(storedUser);
        parsedUser.username = editedUsername.value;
        localStorage.setItem("user", JSON.stringify(parsedUser));
      } catch (err) {
        console.error("Gagal update user di localStorage:", err);
      }
    }

    showEditForm.value = false;
    message.value = "Profil berhasil diperbarui!";
    Swal.fire("Berhasil!", "Profil berhasil diperbarui.", "success");
  } catch (err: any) {
    error.value = err.response?.data?.message || "Gagal memperbarui profil.";
  }
};
</script>


<template>
  <section id="Profil" class="container md:w-[700px] py-24 sm:py-32">
    <div class="text-center mb-8">
      <h2 class="text-3xl md:text-4xl text-center font-bold">Profil Pengguna</h2>
    </div>
    <Accordion type="single" collapsible class="AccordionRoot">
      <AccordionItem
        v-for="{ question, answer, value } in ProfilList"
        :key="value"
        :value="value">
        <AccordionTrigger class="text-left">{{ question }}</AccordionTrigger>
        <AccordionContent>
          <div v-if="value === 'item-2'">
            <div v-if="userProducts.length === 0">Belum ada produk disimpan.</div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
              <div
                v-for="(product, index) in userProducts"
                :key="index"
                class="border rounded-lg p-4 shadow hover:shadow-lg transition">
                <img
                  :src="product.imageUrl"
                  alt="gambar produk"
                  class="w-full h-40 object-cover rounded mb-2"/>
                <h4 class="font-semibold text-lg">{{ product.name }}</h4>
                <p class="text-blue-700 font-medium">{{ product.price }}</p>
                <a
                  :href="product.url"
                  target="_blank"
                  class="text-sm text-blue-500 hover:underline mt-2 block">
                  Lihat Produk
                </a>
                <button
                  class="mt-2 text-red-600 hover:underline text-sm"
                  @click="deleteProduct(product.url)">
                  Hapus Produk
                </button>
              </div>
            </div>
          </div>
          <div v-else>{{ answer }}</div>
        </AccordionContent>
      </AccordionItem>
    </Accordion>

    <h3 class="font-medium mt-4">
      Edit Username?
      <a href="#" class="underline ml-2" @click.prevent="showEditForm = !showEditForm">
        Edit Username
      </a>
    </h3>

    <div v-if="showEditForm" class="mt-4 border p-4 rounded-md space-y-4">
      <label class="block font-medium">Username Baru</label>
      <input
        v-model="editedUsername"
        type="text"
        class="w-full p-2 border rounded-md"/>
      <button
        class="bg-blue-600 text-white px-4 py-2 rounded-md"
        @click="saveUsername">
        Simpan
      </button>
      <p v-if="message" class="text-green-600">{{ message }}</p>
      <p v-if="error" class="text-red-600">{{ error }}</p>
    </div>
  </section>
</template>
