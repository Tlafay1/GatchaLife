<script setup lang="ts">
import MobileNav from '@/components/MobileNav.vue';
</script>

<template>
  <div class="min-h-screen bg-background font-sans antialiased pb-20 md:pb-0">
    <router-view />
    <div class="md:hidden">
      <MobileNav />
    </div>
  </div>
</template>

<style scoped></style>
