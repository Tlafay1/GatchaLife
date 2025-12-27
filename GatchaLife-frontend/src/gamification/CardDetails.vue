<script setup lang="ts">
import { useCardDetails, useRerollCardImage, useCardPreview } from '@/lib/api-client';
import { useRoute } from 'vue-router';
import { ref, computed } from 'vue';
import { Maximize2, X, RefreshCw, Loader2, Lock, Sparkles } from 'lucide-vue-next';

const route = useRoute();
const cardId = Number(route.params.id);
const isPreview = route.name === 'card-preview';

const { data: detailsData, isLoading: detailsLoading } = useCardDetails(isNaN(cardId) ? 0 : cardId);
// Ensure we pass string params correctly
const previewParams = computed(() => route.query as Record<string, string>);
const { data: previewData, isLoading: previewLoading } = useCardPreview(isPreview ? previewParams.value : {});

const item = computed(() => isPreview ? previewData.value : detailsData.value);
const isLoading = computed(() => isPreview ? previewLoading.value : detailsLoading.value);

const { mutate: rerollImage, isPending: isRerolling } = useRerollCardImage();
const isFullScreen = ref(false);

const handleReroll = () => {
  if (confirm('Are you sure you want to regenerate this image? This will replace the current image for everyone.')) {
    rerollImage(cardId);
  }
};

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
        <div class="flex flex-col gap-4">
          <div
            class="relative aspect-[2/3] bg-gray-900 rounded-xl border-4 shadow-2xl overflow-hidden group cursor-pointer"
            :class="rarityColor(item.card.rarity_name)" @click="item.card.image_url ? isFullScreen = true : null">
            <template v-if="item.card.image_url">
                <img :src="item.card.image_url"
                class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" />
            </template>
            <template v-else-if="item.count > 0 && !item.card.image_url">
              <div
                class="w-full h-full bg-slate-900 flex flex-col items-center justify-center p-4 text-center select-none">
                <div class="mb-4 relative">
                  <div class="w-16 h-16 rounded-full border-4 border-slate-700/50 border-t-secondary animate-spin">
                  </div>
                  <div class="absolute inset-0 flex items-center justify-center">
                    <Sparkles class="w-6 h-6 text-secondary animate-pulse" />
                  </div>
                </div>
                <span
                  class="text-xs uppercase font-bold text-secondary tracking-widest animate-pulse">Generating...</span>
              </div>
            </template>
            <template v-else>
               <div class="w-full h-full bg-slate-900 flex flex-col items-center justify-center p-4 text-center select-none bg-[radial-gradient(#333_1px,transparent_1px)] [background-size:16px_16px]">
                  <div class="w-16 h-16 rounded-full bg-slate-800 flex items-center justify-center mb-4 border border-slate-700">
                    <Lock class="w-8 h-8 text-slate-500" />
                  </div>
                  <span class="text-xs uppercase font-bold text-slate-500 tracking-widest">Locked</span>
               </div>
            </template>
          </div>

          <button @click="handleReroll" :disabled="isRerolling || item.count === 0"
            class="w-full py-3 bg-secondary hover:bg-secondary/80 rounded-lg font-bold flex items-center justify-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed">
            <Loader2 v-if="isRerolling" class="w-4 h-4 animate-spin" />
            <RefreshCw v-else class="w-4 h-4" />
            {{ isRerolling ? 'Regenerating...' : 'Regenerate Image' }}
          </button>
          <p v-if="item.count === 0" class="text-xs text-center text-muted-foreground">You must own this card to generate its image.</p>
        </div>

        <!-- Details -->
        <div class="space-y-8">
          <div>
            <div class="flex items-center gap-2 mb-2">
                 <div class="text-sm font-bold uppercase tracking-wider opacity-70" :class="rarityColor(item.card.rarity_name).split(' ')[0]">
                  {{ item.card.rarity_name }}
                </div>
                <div v-if="item.count === 0" class="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-[10px] uppercase font-bold text-slate-400">
                    Locked
                </div>
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
          
          <div v-if="item.card.pose" class="bg-card border border-border rounded-lg p-4">
              <div class="text-xs text-muted-foreground uppercase tracking-wider mb-1">Pose (Prompt)</div>
              <div class="italic text-sm">{{ item.card.pose }}</div>
          </div>

          <div v-if="item.card.description || item.card.visual_override" class="space-y-4">
            <div v-if="item.card.description">
               <div class="text-xs text-muted-foreground uppercase tracking-wider mb-1">Narrative Description</div>
               <p class="text-sm border-l-2 pl-3 border-primary/50">{{ item.card.description }}</p>
            </div>
            <div v-if="item.card.visual_override" class="bg-muted/30 p-3 rounded text-xs font-mono">
               <div class="text-[10px] text-muted-foreground uppercase tracking-wider mb-1">Visual Override</div>
               {{ item.card.visual_override }}
            </div>
          </div>

          <div class="bg-card border border-border rounded-lg p-6">
            <div class="flex justify-between items-center mb-4">
              <div class="font-bold text-lg">Collection Stats</div>
              <div class="px-3 py-1 rounded-full text-sm font-bold"
                 :class="item.count > 0 ? 'bg-secondary text-secondary-foreground' : 'bg-muted text-muted-foreground'">
                {{ item.count > 0 ? `x${item.count} Owned` : 'Not Owned' }}
              </div>
            </div>
            <div class="text-sm text-muted-foreground">
              {{ item.count > 0 ? `Obtained on ${new Date(item.obtained_at).toLocaleDateString()}` : 'You have not discovered this card yet.' }}
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
