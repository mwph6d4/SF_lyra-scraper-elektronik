import path from "path";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

import tailwind from "tailwindcss";
import autoprefixer from "autoprefixer";

export default defineConfig({
    plugins: [vue()],
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },  
    server: {
        proxy: {
            '/api': {
                target: 'http://localhost:5000',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, ''),
            },
        },
    },
  css: {
    postcss: {
      plugins: [tailwind(), autoprefixer()],
    },
  },
});

  // plugins: [vue()],
  // resolve: {
  //   alias: {
  //     "@": path.resolve(__dirname, "./src"),
  //   },
  // },


// export default defineConfig({
//     plugins: [vue()],
//     server: {
//         proxy: {
//             '/api': {
//                 target: 'http://localhost:5000',
//                 changeOrigin: true,
//                 rewrite: path => path.replace(/^\/api/, '')
//             }
//         }
//     }
// });
