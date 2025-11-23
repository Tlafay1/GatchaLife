<script setup lang="ts">
import { useCardDetails } from '@/lib/api-client';
import { useRoute } from 'vue-router';

const route = useRoute();
const cardId = Number(route.params.id);

const { data: item, isLoading } = useCardDetails(cardId);

const rarityColor = (rarity: string) => {
  switch (rarity?.toLowerCase()) {
    case 'common': return 'text-gray-400 border-gray-400 shadow-gray-400/50';
    case 'rare': return 'text-blue-400 border-blue-400 shadow-blue-400/50';
    case 'epic': return 'text-purple-400 border-purple-400 shadow-purple-400/50';
    case 'legendary': return 'text-yellow-400 border-yellow-400 shadow-yellow-400/50';
    default: return 'text-white border-white';
  }
};
</script>

<template>
  <div class="min-h-screen bg-background text-foreground p-8 font-sans flex flex-col items-center">
    <div class="w-full max-w-4xl">
      <router-link to="/collection" class="text-muted-foreground hover:text-foreground transition-colors mb-8 inline-block">
        ← Back to Collection
      </router-link>

      <div v-if="isLoading" class="text-center py-12 text-muted-foreground">
        Loading card details...
      </div>

      <div v-else-if="!item" class="text-center py-12 text-muted-foreground">
        Card not found.
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-12 items-start">
        <!-- Card Image -->
        <div 
          class="relative aspect-[2/3] bg-gray-900 rounded-xl border-4 shadow-2xl overflow-hidden"
          :class="rarityColor(item.card.rarity_name)"
        >
          <img 
            v-if="item.card.image_url" 
            :src="item.card.image_url" 
            class="w-full h-full object-cover"
          />
          <div v-else class="w-full h-full flex items-center justify-center text-muted-foreground">
            No Image
          </div>
        </div>

        <!-- Details -->
        <div class="space-y-8">
          <div>
            <div class="text-sm font-bold uppercase tracking-wider opacity-70 mb-2" :class="rarityColor(item.card.rarity_name).split(' ')[0]">
              {{ item.card.rarity_name }}
            </div>
            <h1 class="text-4xl font-bold mb-2">{{ item.card.character_variant_name }}</h1>
            <div class="text-xl text-muted-foreground">{{ item.card.character_name }}</div>
          </div>

          <div class="grid grid-cols-2 gap-6">
            <div class="bg-card border border-border rounded-lg p-4">
              <div class="text-xs text-muted-foreground uppercase tracking-wider mb-1">Style</div>
              <div class="font-bold">{{ item.card.style_name }}</div>
            </div>
            <div class="bg-card border border-border rounded-lg p-4">
              <div class="text-xs text-muted-foreground uppercase tracking-wider mb-1">Theme</div>
              <div class="font-bold">{{ item.card.theme_name }}</div>
            </div>
          </div>

          <div class="bg-card border border-border rounded-lg p-6">
            <div class="flex justify-between items-center mb-4">
              <div class="font-bold text-lg">Collection Stats</div>
              <div class="bg-secondary text-secondary-foreground px-3 py-1 rounded-full text-sm font-bold">
                x{{ item.count }} Owned
              </div>
            </div>
            <div class="text-sm text-muted-foreground">
              Obtained on {{ new Date(item.obtained_at).toLocaleDateString() }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
