<script setup lang="ts">
import { useCollection } from '@/lib/api-client';
import { ref, computed } from 'vue';

const filters = ref({
  rarity: '',
});

const { data: collection, isLoading } = useCollection(filters);

const rarityColor = (rarity: string) => {
  switch (rarity?.toLowerCase()) {
    case 'common': return 'border-gray-500/50 shadow-gray-500/20';
    case 'rare': return 'border-blue-500/50 shadow-blue-500/20';
    case 'epic': return 'border-purple-500/50 shadow-purple-500/20';
    case 'legendary': return 'border-yellow-500/50 shadow-yellow-500/20';
    default: return 'border-border';
  }
};
</script>

<template>
  <div class="min-h-screen bg-background text-foreground p-8 font-sans">
    <div class="max-w-6xl mx-auto space-y-8">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <h1 class="text-3xl font-bold">Collection</h1>
        <router-link to="/" class="text-muted-foreground hover:text-foreground transition-colors">
          ← Back to Dashboard
        </router-link>
      </div>

      <!-- Filters -->
      <div class="flex gap-4 overflow-x-auto pb-2">
        <button 
          @click="filters.rarity = ''"
          class="px-4 py-2 rounded-full border transition-colors"
          :class="!filters.rarity ? 'bg-primary text-primary-foreground border-primary' : 'bg-card border-border hover:border-primary/50'"
        >
          All
        </button>
        <button 
          v-for="r in ['Common', 'Rare', 'Epic', 'Legendary']" 
          :key="r"
          @click="filters.rarity = r"
          class="px-4 py-2 rounded-full border transition-colors"
          :class="filters.rarity === r ? 'bg-primary text-primary-foreground border-primary' : 'bg-card border-border hover:border-primary/50'"
        >
          {{ r }}
        </button>
      </div>

      <!-- Grid -->
      <div v-if="isLoading" class="text-center py-12 text-muted-foreground">
        Loading collection...
      </div>
      
      <div v-else-if="!collection?.length" class="text-center py-12 text-muted-foreground bg-card rounded-xl border border-border">
        No cards found. Go summon some!
      </div>

      <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
        <div 
          v-for="item in collection" 
          :key="item.id"
          class="group relative aspect-[2/3] bg-card rounded-xl border-2 overflow-hidden transition-all hover:scale-105 hover:z-10"
          :class="rarityColor(item.card.rarity_name)"
        >
          <!-- Image -->
          <div class="absolute inset-0 bg-muted">
            <img 
              v-if="item.card.image_url" 
              :src="item.card.image_url" 
              class="w-full h-full object-cover transition-transform group-hover:scale-110"
              loading="lazy"
            />
            <div v-else class="w-full h-full flex items-center justify-center text-muted-foreground text-xs">
              Generating...
            </div>
          </div>

          <!-- Overlay Info -->
          <div class="absolute inset-x-0 bottom-0 p-3 bg-gradient-to-t from-black/90 via-black/60 to-transparent pt-12 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-end">
            <div class="text-xs font-bold text-white/80 uppercase">{{ item.card.rarity_name }}</div>
            <div class="font-bold text-white text-sm leading-tight">{{ item.card.character_variant_name }}</div>
            <div class="text-xs text-white/60 mt-1">x{{ item.count }}</div>
          </div>

          <!-- Count Badge (always visible) -->
          <div v-if="item.count > 1" class="absolute top-2 right-2 bg-black/60 backdrop-blur text-white text-xs font-bold px-2 py-1 rounded-full border border-white/20">
            x{{ item.count }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
