<script setup lang="ts">
import { ref, onMounted } from 'vue';

const props = defineProps<{
  drop: any;
}>();

const emit = defineEmits(['close']);

const step = ref('summoning'); // summoning, revealed

onMounted(() => {
  setTimeout(() => {
    step.value = 'revealed';
  }, 2000); // 2 seconds of animation
});

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
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-sm" @click="step === 'revealed' ? emit('close') : null">
    
    <!-- Summoning Animation -->
    <div v-if="step === 'summoning'" class="flex flex-col items-center gap-4 animate-pulse">
      <div class="w-32 h-32 rounded-full bg-gradient-to-r from-purple-500 to-blue-500 animate-spin blur-xl"></div>
      <div class="text-2xl font-bold text-white tracking-widest uppercase">Summoning...</div>
    </div>

    <!-- Revealed Card -->
    <div v-else class="relative flex flex-col items-center gap-6 animate-in zoom-in duration-500">
      <div 
        class="relative w-80 aspect-[2/3] bg-gray-800 rounded-xl border-4 shadow-2xl overflow-hidden flex flex-col"
        :class="rarityColor(drop?.card?.rarity_name)"
      >
        <!-- Image -->
        <div class="flex-1 bg-gray-900 relative">
          <img 
            v-if="drop?.card?.image_url" 
            :src="drop.card.image_url" 
            class="absolute inset-0 w-full h-full object-cover"
          />
          <div v-else class="absolute inset-0 flex items-center justify-center text-muted-foreground">
            No Image
          </div>
        </div>
        
        <!-- Info -->
        <div class="p-4 bg-black/80 backdrop-blur-md border-t border-white/10">
          <div class="text-xs font-bold uppercase tracking-wider opacity-70 mb-1">{{ drop?.card?.rarity_name }}</div>
          <h3 class="text-lg font-bold text-white leading-tight">{{ drop?.card?.character_variant_name }}</h3>
          <div class="text-sm text-gray-400">{{ drop?.card?.style_name }} • {{ drop?.card?.theme_name }}</div>
        </div>
      </div>

      <div class="text-center space-y-2">
        <h2 class="text-3xl font-bold text-white drop-shadow-lg">
          {{ drop?.is_new ? 'NEW CARD!' : 'DUPLICATE' }}
        </h2>
        <p class="text-gray-400">Tap anywhere to close</p>
      </div>
    </div>

  </div>
</template>
