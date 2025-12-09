<script setup lang="ts">
import { usePlayerStats, useGatchaRoll } from '@/lib/api-client';
import { ref } from 'vue';
import { Sparkles, Gem } from 'lucide-vue-next';
import GatchaAnimation from '@/gamification/GatchaAnimation.vue';

const { data: player, refetch: refetchPlayer } = usePlayerStats();
const { mutate: rollGatcha, isPending: isRolling } = useGatchaRoll();

const showGatcha = ref(false);
const dropData = ref<Array<{
  card: {
    rarity_name: string;
    image_url?: string;
    character_variant_name: string;
    style_name: string;
    theme_name: string;
  };
  is_new: boolean;
}> | null>(null);

const handleRoll = () => {
  rollGatcha(undefined, {
    onSuccess: (data) => {
      dropData.value = data.drops;
      showGatcha.value = true;
      refetchPlayer(); // Update coins immediately
    },
    onError: (err) => {
      alert(err.message);
    }
  });
};

const closeGatcha = () => {
  showGatcha.value = false;
  dropData.value = null;
  refetchPlayer();
};
</script>

<template>
  <div>
    <div class="relative overflow-hidden rounded-3xl bg-card border border-border shadow-lg group">
      <!-- Banner Image (Placeholder or generated) -->
      <div class="absolute inset-0 bg-gradient-to-r from-slate-900 to-slate-800 z-0">
        <!-- Abstract shapes -->
        <div
          class="absolute -top-24 -right-24 w-64 h-64 bg-purple-500/30 rounded-full blur-3xl group-hover:bg-purple-500/40 transition-colors duration-500">
        </div>
        <div
          class="absolute -bottom-24 -left-24 w-64 h-64 bg-blue-500/30 rounded-full blur-3xl group-hover:bg-blue-500/40 transition-colors duration-500">
        </div>
      </div>

      <div class="relative z-10 p-8 sm:p-12 flex flex-col items-center text-center space-y-6">
        <div
          class="w-24 h-24 rounded-2xl bg-gradient-to-br from-purple-500 to-pink-500 shadow-lg shadow-purple-500/30 flex items-center justify-center transform rotate-3 group-hover:rotate-6 transition-transform duration-500">
          <Sparkles class="w-12 h-12 text-white" />
        </div>

        <div class="space-y-2 max-w-lg">
          <h3 class="text-3xl font-black text-white">Standard Banner</h3>
          <p class="text-slate-300">Summon unique AI-generated characters. Collect Common, Rare, and Legendary
            variants!</p>
        </div>

        <button @click="handleRoll" :disabled="isRolling || (player?.gatcha_coins < 100)"
          class="w-full max-w-xs py-4 bg-white hover:bg-slate-50 text-slate-900 rounded-xl font-black text-lg shadow-xl shadow-white/10 transition-all hover:scale-105 active:scale-95 disabled:opacity-50 disabled:scale-100 flex items-center justify-center gap-2">
          <span v-if="isRolling" class="animate-spin">↻</span>
          <Gem v-else class="w-5 h-5" />
          {{ isRolling ? 'Summoning...' : 'Summon x5' }}
        </button>
      </div>
    </div>

    <GatchaAnimation v-if="showGatcha && dropData" :drops="dropData" @close="closeGatcha" />
  </div>
</template>
