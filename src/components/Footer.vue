<script setup lang="ts">
import { ChevronsDown } from "lucide-vue-next";
import Separator from "./ui/separator/Separator.vue";
</script>

<template>
  <footer
    id="footer"
    class="container py-24 pb-16 sm:py-32 sm:pb-24"
  >
    <div class="p-10 bg-muted/50 dark:bg-card border rounded-2xl">
      <div
        class="grid grid-cols-2 md:grid-cols-4 xl:grid-cols-6 gap-x-12 gap-y-8"
      >
        <div class="col-span-full xl:col-span-2">
          <a
            href="#"
            class="flex font-bold items-center"
          >
            <ChevronsDown
              class="bg-gradient-to-tr from-primary via-primary/70 to-primary rounded-lg w-9 h-9 mr-2 border text-white"
            />

            <h3 class="text-2xl">YourBestPrice</h3>
          </a>
        </div>

        <!-- <div class="flex flex-col gap-2">
          <h3 class="font-bold text-lg">Contact</h3>
          <div>
            <a
              href="#"
              class="opacity-60 hover:opacity-100"
            >
              Github
            </a>
          </div>

          <div>
            <a
              href="#"
              class="opacity-60 hover:opacity-100"
            >
              Twitter
            </a>
          </div>

          <div>
            <a
              href="#"
              class="opacity-60 hover:opacity-100"
            >
              Instagram
            </a>
          </div>
        </div> -->

        <!-- <div class="flex flex-col gap-2">
          <h3 class="font-bold text-lg">Platforms</h3>
          <div>
            <a
              href="#"
              class="opacity-60 hover:opacity-100"
            >
              iOS
            </a>
          </div>

          <div>
            <a
              href="#"
              class="opacity-60 hover:opacity-100"
            >
              Android
            </a>
          </div>

          <div>
            <a
              href="#"
              class="opacity-60 hover:opacity-100"
            >
              Web
            </a>
          </div>
        </div> -->

        <!-- <div class="flex flex-col gap-2">
          <h3 class="font-bold text-lg">Help</h3>
          <div>
            <a
              href="#"
              class="opacity-60 hover:opacity-100"
            >
              Contact Us
            </a>
          </div>

          <div>
            <a
              href="#"
              class="opacity-60 hover:opacity-100"
            >
              FAQ
            </a>
          </div>

          <div>
            <a
              href="#"
              class="opacity-60 hover:opacity-100"
            >
              Feedback
            </a>
          </div>
        </div> -->

        <!-- <div class="flex flex-col gap-2">
          <h3 class="font-bold text-lg">Online-Shop</h3>
          <div>
            <a
              href="https://www.shopee.co.id/"
              class="opacity-60 hover:opacity-100"
            >
              Shopee
            </a>
          </div>

          <div>
            <a
              href="https://www.google.com/aclk?sa=l&ai=DChcSEwjQwIbZuKONAxVThUsFHa4DGsgYABABGgJzZg&co=1&gclid=CjwKCAjw_pDBBhBMEiwAmY02NvZuGqGoFAHAIomd60uzYJmQYJO6PwbTeVsX08KW2xuYldJ6xwgodhoCJrEQAvD_BwE&category=acrcp_v1_0&sig=AOD64_1Fl7OOauqsreORwy-oRZbvkF8uYA&q&adurl&ved=2ahUKEwjW3oLZuKONAxXozjgGHVBcBxYQ0Qx6BAgKEAE"
              class="opacity-60 hover:opacity-100"
            >
              Lazada
            </a>
          </div>

          <div>
            <a
              href="https://www.tokopedia.com/"
              class="opacity-60 hover:opacity-100"
            >
              Tokopedia
            </a>
          </div>
        </div> -->
      </div>

      <Separator class="my-6" />
      <section className="">
        <h3 class="">
          &copy; 2024 Designed and developed by
          <a
            target="_blank"
            href="https://github.com/leoMirandaa"
            className="text-primary transition-all border-primary hover:border-b-2"
          >
            Leo Miranda
          </a>
        </h3>
      </section>
    </div>
  </footer>
</template>
