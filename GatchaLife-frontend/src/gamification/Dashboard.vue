<script setup lang="ts">
import { usePlayerStats, useSyncTickTick, useGatchaRoll } from '@/lib/api-client';
import { ref } from 'vue';
import GatchaAnimation from './GatchaAnimation.vue';

const { data: player, refetch: refetchPlayer } = usePlayerStats();
const { mutate: syncTickTick, isPending: isSyncing } = useSyncTickTick();
const { mutate: rollGatcha, isPending: isRolling } = useGatchaRoll();

const showGatcha = ref(false);
const dropData = ref(null);

const handleSync = () => {
  syncTickTick(undefined, {
    onSuccess: (data) => {
      // Show some notification about XP gained
      console.log('Synced!', data);
    }
  });
};

const handleRoll = () => {
  rollGatcha(undefined, {
    onSuccess: (data) => {
      dropData.value = data.drop;
      showGatcha.value = true;
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
  <div class="min-h-screen bg-background text-foreground p-8 font-sans">
    <div class="max-w-4xl mx-auto space-y-8">
      <!-- Header / Stats -->
      <div class="bg-card border border-border rounded-xl p-6 shadow-lg flex items-center justify-between">
        <div class="flex items-center gap-4">
          <div class="h-16 w-16 rounded-full bg-primary flex items-center justify-center text-2xl font-bold text-primary-foreground">
            {{ player?.level || 1 }}
          </div>
          <div>
            <h1 class="text-2xl font-bold">{{ player?.user?.username || 'Player' }}</h1>
            <div class="text-muted-foreground">Level {{ player?.level || 1 }}</div>
          </div>
        </div>
        
        <div class="flex gap-8 text-center">
          <div>
            <div class="text-sm text-muted-foreground uppercase tracking-wider">XP</div>
            <div class="text-xl font-mono font-bold text-accent-foreground">{{ player?.xp || 0 }}</div>
          </div>
          <div>
            <div class="text-sm text-muted-foreground uppercase tracking-wider">Coins</div>
            <div class="text-xl font-mono font-bold text-yellow-500">{{ player?.gatcha_coins || 0 }}</div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Quests / Sync -->
        <div class="bg-card border border-border rounded-xl p-6 shadow-lg space-y-4">
          <h2 class="text-xl font-bold flex items-center gap-2">
            <span class="i-lucide-check-circle text-green-500"></span>
            Daily Tasks
          </h2>
          <p class="text-muted-foreground">Sync with TickTick to claim rewards.</p>
          <button 
            @click="handleSync" 
            :disabled="isSyncing"
            class="w-full py-3 px-4 bg-secondary hover:bg-secondary/80 text-secondary-foreground rounded-lg font-bold transition-all flex items-center justify-center gap-2"
          >
            <span v-if="isSyncing" class="animate-spin">↻</span>
            {{ isSyncing ? 'Syncing...' : 'Sync TickTick' }}
          </button>
        </div>

        <!-- Gatcha -->
        <div class="bg-card border border-border rounded-xl p-6 shadow-lg space-y-4 relative overflow-hidden group">
          <div class="absolute inset-0 bg-gradient-to-br from-purple-500/10 to-blue-500/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <h2 class="text-xl font-bold flex items-center gap-2">
            <span class="i-lucide-sparkles text-purple-500"></span>
            Summon
          </h2>
          <p class="text-muted-foreground">Spend 100 coins to summon a new card.</p>
          <button 
            @click="handleRoll"
            :disabled="isRolling || (player?.gatcha_coins < 100)"
            class="w-full py-3 px-4 bg-primary hover:bg-primary/90 text-primary-foreground rounded-lg font-bold transition-all shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Summon (100 Coins)
          </button>
        </div>
      </div>

      <!-- Navigation -->
      <div class="flex justify-center gap-4">
        <router-link to="/collection" class="px-6 py-2 rounded-full bg-muted text-muted-foreground hover:bg-muted/80 transition-colors">
          View Collection
        </router-link>
      </div>
    </div>

    <!-- Gatcha Overlay -->
    <GatchaAnimation 
      v-if="showGatcha" 
      :drop="dropData" 
      @close="closeGatcha" 
    />
  </div>
</template>
