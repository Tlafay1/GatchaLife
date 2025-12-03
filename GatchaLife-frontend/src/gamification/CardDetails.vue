<script setup lang="ts">
import { useCardDetails } from '@/lib/api-client';
import { useRoute } from 'vue-router';
import { ref } from 'vue';
import { Maximize2, X } from 'lucide-vue-next';

const route = useRoute();
const cardId = Number(route.params.id);

const { data: item, isLoading } = useCardDetails(cardId);
const isFullScreen = ref(false);

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
          class="relative aspect-[2/3] bg-gray-900 rounded-xl border-4 shadow-2xl overflow-hidden group cursor-pointer"
          :class="rarityColor(item.card.rarity_name)"
          @click="isFullScreen = true"
        >
          <img 
            v-if="item.card.image_url" 
            :src="item.card.image_url" 
            class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          />
          <div v-else class="w-full h-full flex items-center justify-center text-muted-foreground">
            No Image
          </div>

          <!-- Expand Overlay -->
          <div class="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
            <div class="bg-black/50 p-3 rounded-full backdrop-blur-sm text-white">
              <Maximize2 class="w-6 h-6" />
            </div>
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

    <!-- Full Screen Modal -->
    <Teleport to="body">
      <div v-if="isFullScreen && item" class="fixed inset-0 z-50 flex items-center justify-center bg-black/95 backdrop-blur-sm p-4"
        @click="isFullScreen = false">
        
        <button @click="isFullScreen = false" class="absolute top-4 right-4 p-2 text-white/70 hover:text-white bg-white/10 hover:bg-white/20 rounded-full transition-colors z-50">
          <X class="w-8 h-8" />
        </button>

        <div class="relative w-full h-full max-w-5xl max-h-[90vh] flex items-center justify-center" @click.stop>
          <img 
            v-if="item.card.image_url" 
            :src="item.card.image_url" 
            class="max-w-full max-h-full object-contain rounded-lg shadow-2xl"
          />
        </div>
      </div>
    </Teleport>
  </div>
</template>
