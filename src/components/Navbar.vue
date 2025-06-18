<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useColorMode } from "@vueuse/core";
import { eventBus } from "@/EventBus";
import { useRoute } from 'vue-router'
import axios from "axios";
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
} from "@/components/ui/navigation-menu";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search } from "lucide-vue-next";
import ToggleTheme from "./ToggleTheme.vue";
import { useRouter } from "vue-router";

const mode = useColorMode();
mode.value = "light";

const router = useRouter();

interface UserProps {
  username: string;
  id: number;
}

const route = useRoute()

const isActive = (path: string) => {
  return route.path === path
}

const user = ref<UserProps | null>(null);

function getUser() {
  const stored = localStorage.getItem("user");
  if (stored) {
    try {
      user.value = JSON.parse(stored);
    } catch (err) {
      console.error("Error parsing user JSON:", err);
      user.value = null;
    }
  } else {
    user.value = null;
  }
}

onMounted(() => {
  getUser();
  fetchCategories();
  eventBus.on("user-logged-in", getUser);
  eventBus.on("user-logged-out", getUser);
});

onUnmounted(() => {
  eventBus.off("user-logged-in", getUser);
  eventBus.off("user-logged-out", getUser);
});

function logout() {
  localStorage.removeItem("user");
  localStorage.removeItem("token");
  user.value = null;
  eventBus.emit("user-logged-out");
  router.push("/");
}

function profil() {
  router.push("/profil");
}

function disimpan() {
  router.push("/disimpan");
}

interface RouteProps {
  href: string;
  label: string;
}

interface CategoryProps {
  name: string;
  slug: string;
}

const routeList: RouteProps[] = [
  {
    href: "/product",
    label: "Product",
  },
];

const categoryList = ref<CategoryProps[]>([]);

async function fetchCategories() {
  try {
    const res = await axios.get("http://localhost:5000/api/categories");
    console.log("Kategori dari backend:", res.data);
    categoryList.value = res.data;
  } catch (err) {
    console.error("Gagal mengambil kategori:", err);
  }
}

const isOpen = ref<boolean>(false);
const searchQuery = ref("");

// const emitSearch = () => {
//   router.push({ path: "/product", query: { q: searchQuery.value } });
// };

const emitSearch = async () => {
  const query = searchQuery.value.trim();
  if (!query) return;

  const storedUser = localStorage.getItem("user");
  const userData = storedUser ? JSON.parse(storedUser) : null;

  // Kirim pencarian ke backend jika user login
  if (userData && userData.id) {
    try {
      await axios.post("http://localhost:5000/api/search-history", {
        user_id: userData.id,
        query: query
      });
    } catch (err) {
      console.error("Gagal menyimpan histori pencarian:", err);
    }
  }

  // Redirect ke halaman product dengan query pencarian
  router.push({ path: "/product", query: { q: query } });
};


// function goToCategory(slug: string) {
//   router.push({ path: "/product", query: { kategori: slug } });
// }
</script>

<template>
  <header
    :class="{
      'shadow-light': mode === 'light',
      'shadow-dark': mode === 'dark',
      'w-[90%] md:w-[70%] lg:w-[75%] lg:max-w-screen-xl top-5 mx-auto sticky border z-40 rounded-2xl flex justify-between items-center p-2 bg-card shadow-md': true,
    }"
  >
    <img src="@/assets/logo2.png" alt="Logo" class="bg-gradient-to-tr from-primary via-primary/70 to-primary rounded-lg w-50 h-10 mr-2" />

    <!-- Desktop Navigation -->
    <NavigationMenu class="hidden lg:block">
      <NavigationMenuList>
        <!-- Home -->
        <NavigationMenuItem>
          <NavigationMenuLink asChild>
            <Button as-child variant="ghost" class="justify-start text-base">
              <router-link
                to="/home"
                :class="[
                  'px-4 py-2 rounded-md text-base hover:bg-muted',
                  isActive('/home') ? 'text-primary font-semibold underline underline-offset-4' : ''
                ]">
                Home
              </router-link>
            </Button>
          </NavigationMenuLink>
        </NavigationMenuItem>

        <!-- Route Buttons -->
        <NavigationMenuItem>
          <NavigationMenuLink asChild>
            <Button
              v-for="{ href, label } in routeList"
              :key="label"
              as-child
              variant="ghost"
              class="justify-start text-base"
            >
            <router-link
              :to="href"
              :class="[
                isActive(href) ? 'text-primary font-semibold underline underline-offset-4' : '',
                'px-4 py-2 rounded-md text-base hover:bg-muted'
              ]"
            >
              {{ label }}
            </router-link>
            </Button>
          </NavigationMenuLink>
        </NavigationMenuItem>
      </NavigationMenuList>
    </NavigationMenu>

    <!-- Search Bar -->
    <div class="relative">
      <Search class="absolute left-2 top-3 h-4 w-4 text-muted-foreground" />
      <Input
        v-model="searchQuery"
        @keydown.enter="emitSearch"
        type="search"
        placeholder="Cari produk..."
        class="w-48 rounded-lg bg-background pl-9 pr-4 py-2 text-sm focus:w-64 transition-all duration-300"
      />
    </div>

    <!-- User Info Dropdown -->
    <NavigationMenu>
      <NavigationMenuList>
        <NavigationMenuItem v-if="user">
          <NavigationMenuTrigger class="bg-card text-base px-4 py-2 rounded-md hover:bg-muted text-orange-500">
            Hai {{ user.username }} !
          </NavigationMenuTrigger>
          <NavigationMenuContent>
            <ul class="w-40 p-2 space-y-2">
              <li>
                <button @click="profil" class="w-full text-left px-3 py-2 rounded-md hover:bg-muted text-sm font-medium">
                  Profil
                </button>
              </li>
              <li>
                <button @click="disimpan" class="w-full text-left px-3 py-2 rounded-md hover:bg-muted text-sm font-medium">
                  Produk Disimpan
                </button>
              </li>
              <li>
                <button @click="logout" class="w-full text-left px-3 py-2 rounded-md hover:bg-muted text-sm font-medium">
                  Logout
                </button>
              </li>
            </ul>
          </NavigationMenuContent>
        </NavigationMenuItem>
        <NavigationMenuItem v-else>
          <NavigationMenuLink asChild>
            <router-link to="/login" class="px-4 py-2 rounded-md text-base hover:bg-muted">
              Login/Register
            </router-link>
          </NavigationMenuLink>
        </NavigationMenuItem>
      </NavigationMenuList>
    </NavigationMenu>

    <!-- Dark Mode Toggle -->
    <div class="hidden lg:flex">
      <ToggleTheme />
    </div>
  </header>
</template>

<style scoped>
.shadow-light {
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.085);
}
.shadow-dark {
  box-shadow: inset 0 0 5px rgba(255, 255, 255, 0.141);
}
</style>
