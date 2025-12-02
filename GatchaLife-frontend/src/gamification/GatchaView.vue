<script setup lang="ts">
import SummonBanner from '@/components/SummonBanner.vue';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-vue-next';
</script>

<template>
  <div class="min-h-screen bg-background text-foreground p-4 md:p-8 font-sans">
    <div class="max-w-4xl mx-auto space-y-8">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-4">
          <router-link to="/" class="hidden md:block">
            <Button variant="ghost" size="icon">
              <ArrowLeft class="w-5 h-5" />
            </Button>
          </router-link>
          <h1 class="text-3xl font-bold">Summon</h1>
        </div>
      </div>

      <!-- Banner -->
      <SummonBanner />
    </div>
  </div>
</template>
