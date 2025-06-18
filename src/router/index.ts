import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/components/Home.vue';
import Product from '@/components/Product.vue';
import Login from '@/components/Login.vue';
import Profil from '@/components/Profil.vue';
import Simpan from '@/components/Simpan.vue';
import Compare from '@/components/Compare.vue'; // tambahkan ini

const routes = [
  { path: "/", redirect: "/home" },
  { path: "/login", component: Login },
  { path: "/product", name: "product", component: Product },
  { path: "/profil", component: Profil },
  { path: "/disimpan", component: Simpan },
  { path: "/compare", component: Compare, meta: { requiresAuth: true } },
  { path: "/home", component: Home }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Middleware untuk proteksi route
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");

  if (to.meta.requiresAuth && !token) {
    next("/login");
  } else {
    next();
  }
});

export default router;
