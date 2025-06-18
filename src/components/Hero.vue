<script setup lang="ts">
// import { useColorMode } from "@vueuse/core";
// const mode = useColorMode();

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-vue-next";
</script>

<template>
  <section class="container">
    <div
      class="grid place-items-center lg:max-w-screen-xl gap-8 mx-auto py-20 md:py-32">
      <div class="text-center space-y-8">
        <Badge
          variant="outline"
          class="text-sm py-2">
          <span class="mr-2 text-primary">
            <Badge>New</Badge>
          </span>
          <span> Experience in Here! </span>
        </Badge>

        <div
          class="max-w-screen-md mx-auto text-center text-5xl md:text-6xl font-bold">
          <h1>
            Find your
            <span
              class="text-transparent bg-gradient-to-r from-[#D247BF] to-primary bg-clip-text"
              >Best Electronics Price
            </span>
            here
          </h1>
        </div>

        <p class="max-w-screen-sm mx-auto text-xl text-muted-foreground">
          Temukan harga elektronik terbaik yang kamu inginkan disini!
        </p>

        <div class="space-y-4 md:space-y-0 md:space-x-4">
          <router-link to="/product">
            <Button class="w-5/6 md:w-1/4 font-bold group/arrow" as-child>
              <span>
                Lihat Produk
                <ArrowRight
                  class="size-5 ml-2 group-hover/arrow:translate-x-1 transition-transform" />
              </span>
            </Button>
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.img-shadow-animation {
  animation-name: img-shadow-animation;
  animation-iteration-count: infinite;
  animation-duration: 2s;
  animation-timing-function: linear;
  animation-direction: alternate;
}

.img-border-animation {
  animation-name: img-border-animation;
  animation-iteration-count: infinite;
  animation-duration: 2s;
  animation-timing-function: linear;
  animation-direction: alternate;
}

@keyframes img-shadow-animation {
  from {
    opacity: 0.5;
    transform: translateY(30px);
  }

  to {
    opacity: 1;
    transform: translateY(0px);
  }
}
/* @keyframes img-border-animation {
  from {
    @apply border-t-primary/10;
  }

  to {
    @apply border-t-primary/60;
  }
}  */
</style>
