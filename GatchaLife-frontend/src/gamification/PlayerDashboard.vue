<script setup lang="ts">
import { usePlayerStats, useGatchaRoll, useTickTickStats, useCollection } from '@/lib/api-client';
import { ref, computed, watch } from 'vue';
import GatchaAnimation from './GatchaAnimation.vue';
import StatCard from '@/components/StatCard.vue';
import LevelUpModal from '@/components/LevelUpModal.vue';
import {
  Coins,
  Sparkles,
  Gem,
  PlusCircle,
  ClipboardList,
  CheckCircle2,
  Library,
  Flame
} from 'lucide-vue-next';

const { data: player, refetch: refetchPlayer } = usePlayerStats();
const { mutate: rollGatcha, isPending: isRolling } = useGatchaRoll();
const { data: stats, isLoading: statsLoading } = useTickTickStats();
const { data: collection } = useCollection();

const showGatcha = ref(false);
const dropData = ref<{
  card: {
    rarity_name: string;
    image_url?: string;
    character_variant_name: string;
    style_name: string;
    theme_name: string;
  };
  is_new: boolean;
} | null>(null);
const showLevelUp = ref(false);

// Watch for level up
watch(() => player.value?.level, (newLevel, oldLevel) => {
  if (oldLevel && newLevel && newLevel > oldLevel) {
    showLevelUp.value = true;
  }
});

const xpPercentage = computed(() => {
  if (!player.value) return 0;
  const maxXp = player.value.level * 100;
  return Math.min((player.value.xp / maxXp) * 100, 100);
});

const handleRoll = () => {
  rollGatcha(undefined, {
    onSuccess: (data) => {
      dropData.value = data.drop;
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
  <div class="min-h-screen bg-background text-foreground pb-20 font-sans selection:bg-primary/30">
    <!-- Top Navigation / Header -->
    <div class="sticky top-0 z-40 border-b border-border/50 bg-background/80 backdrop-blur-xl">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div
            class="h-8 w-8 rounded-lg bg-gradient-to-br from-primary to-purple-600 flex items-center justify-center text-white font-bold shadow-lg shadow-primary/20">
            G
          </div>
          <span class="font-bold text-lg tracking-tight">GatchaLife</span>
        </div>

        <div class="flex items-center gap-4">
          <router-link to="/studio"
            class="p-2 rounded-full hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
            title="Creator Studio">
            <!-- Icon removed or replaced if needed, but PenTool was removed from imports -->
            <span class="text-sm font-bold">Studio</span>
          </router-link>

          <!-- Coin Display -->
          <div class="flex items-center gap-2 bg-secondary/50 px-3 py-1.5 rounded-full border border-border/50">
            <Coins class="w-4 h-4 text-yellow-500" />
            <span class="font-bold font-mono">{{ player?.gatcha_coins || 0 }}</span>
          </div>

          <!-- Profile/Avatar -->
          <div
            class="h-9 w-9 rounded-full bg-muted border border-border flex items-center justify-center text-sm font-bold">
            {{ player?.user?.username?.charAt(0) || 'P' }}
          </div>
        </div>
      </div>
    </div>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">

      <!-- Hero Section -->
      <div
        class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-8 sm:p-12 text-white shadow-2xl border border-white/10">
        <!-- Background Patterns -->
        <div class="absolute top-0 right-0 -mt-20 -mr-20 h-96 w-96 rounded-full bg-primary/20 blur-3xl"></div>
        <div class="absolute bottom-0 left-0 -mb-20 -ml-20 h-80 w-80 rounded-full bg-purple-500/20 blur-3xl"></div>

        <div class="relative z-10 flex flex-col md:flex-row items-center justify-between gap-8">
          <div class="flex-1 text-center md:text-left space-y-4">
            <div
              class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 border border-white/10 text-xs font-bold uppercase tracking-wider text-primary-foreground/80">
              <span class="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
              Online
            </div>
            <h1 class="text-4xl sm:text-5xl font-black tracking-tight">
              Welcome back, <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">{{
                player?.user?.username || 'Player' }}</span>
            </h1>
            <p class="text-lg text-slate-300 max-w-xl">
              Complete real-world tasks to earn XP and Coins. Build your ultimate collection.
            </p>

            <!-- XP Bar -->
            <div class="max-w-md space-y-2 pt-4">
              <div class="flex justify-between text-sm font-bold">
                <span class="text-blue-300">Level {{ player?.level || 1 }}</span>
                <span class="text-slate-400">{{ player?.xp || 0 }} / {{ (player?.level || 1) * 100 }} XP</span>
              </div>
              <div class="relative group cursor-help">
                <div
                  class="h-3 w-full bg-slate-950/50 rounded-full overflow-hidden backdrop-blur-sm border border-white/5">
                  <div
                    class="h-full bg-gradient-to-r from-blue-500 to-purple-500 shadow-[0_0_15px_rgba(59,130,246,0.5)] transition-all duration-1000 ease-out relative overflow-hidden"
                    :style="{ width: `${xpPercentage}%` }">
                    <div
                      class="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent w-full -translate-x-full animate-[shimmer_2s_infinite]">
                    </div>
                  </div>
                </div>

                <!-- Tooltip -->
                <div
                  class="absolute opacity-0 group-hover:opacity-100 transition-opacity bottom-full left-1/2 -translate-x-1/2 mb-2 bg-popover text-popover-foreground text-xs rounded px-2 py-1 shadow-lg whitespace-nowrap z-10 pointer-events-none">
                  {{ player?.xp || 0 }} / {{ (player?.level || 1) * 100 }} XP
                  <div class="text-[10px] text-muted-foreground mt-1 border-t border-border/50 pt-1">
                    Next Level: +0.5% Luck Bonus
                  </div>
                </div>
              </div>

              <div class="text-xs text-slate-500 text-right mb-2 mt-1">
                {{ Math.floor(((player?.level || 1) * 100) - (player?.xp || 0)) }} XP to next level
              </div>

              <div class="flex justify-between text-xs text-muted-foreground font-medium">
                <span>Level {{ player?.level || 1 }}</span>
                <span class="text-primary font-bold">Luck Bonus: +{{ Math.min((player?.level || 1) * 0.5,
                  20).toFixed(1) }}%</span>
                <span>Level {{ (player?.level || 1) + 1 }}</span>
              </div>
            </div>
          </div>

          <!-- Hero Action -->
          <div class="flex flex-col gap-4 min-w-[200px]">
            <!-- Sync button removed as per user request (Zapier handles it now) -->
            <div class="p-4 rounded-xl bg-white/5 border border-white/10 backdrop-blur-sm">
              <div class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Status</div>
              <div class="flex items-center gap-2 text-green-400 font-bold">
                <span class="relative flex h-3 w-3">
                  <span
                    class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                </span>
                Listening for Tasks
              </div>
              <div class="text-xs text-slate-500 mt-2">
                Complete tasks in TickTick to earn rewards automatically.
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8" v-motion-slide-visible-once-bottom>
        <StatCard title="Tasks Completed" :value="stats?.completed_today || 0" :icon="CheckCircle2"
          color="text-green-500" bg-gradient="from-green-500/10 to-transparent" />

        <StatCard title="Gatcha Coins" :value="player?.gatcha_coins || 0" :icon="Coins" color="text-yellow-500"
          bg-gradient="from-yellow-500/10 to-transparent" />

        <StatCard title="Collection" :value="collection?.length || 0" :icon="Library" color="text-purple-500"
          bg-gradient="from-purple-500/10 to-transparent" clickable @click="$router.push('/collection')" />

        <StatCard title="Current Streak" :value="`${stats?.current_streak || 0} Days`" :icon="Flame"
          color="text-orange-500" bg-gradient="from-orange-500/10 to-transparent" />
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">

        <!-- Summon Section -->
        <div class="lg:col-span-2 space-y-6" v-motion :initial="{ opacity: 0, x: -20 }"
          :enter="{ opacity: 1, x: 0, transition: { delay: 400 } }">
          <div class="flex items-center justify-between">
            <h2 class="text-2xl font-bold tracking-tight">Summon Cards</h2>
            <div class="text-sm text-muted-foreground">100 Coins / Roll</div>
          </div>

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
                {{ isRolling ? 'Summoning...' : 'Summon x1' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Recent Activity Feed -->
        <div class="space-y-6" v-motion :initial="{ opacity: 0, x: 20 }"
          :enter="{ opacity: 1, x: 0, transition: { delay: 600 } }">
          <h2 class="text-2xl font-bold tracking-tight">Recent Activity</h2>

          <div class="bg-card border border-border rounded-3xl p-6 shadow-sm min-h-[400px]">
            <div v-if="statsLoading" class="flex justify-center py-8">
              <span class="animate-spin text-muted-foreground">↻</span>
            </div>

            <div v-else-if="stats?.recent_activity?.length" class="space-y-6 relative">
              <!-- Timeline Line -->
              <div class="absolute left-4 top-2 bottom-2 w-0.5 bg-border"></div>

              <div v-for="task in stats.recent_activity" :key="task.id" class="relative pl-10 group">
                <!-- Timeline Dot -->
                <div
                  class="absolute left-[13px] top-1.5 w-2.5 h-2.5 rounded-full bg-green-500 ring-4 ring-background group-hover:scale-125 transition-transform">
                </div>

                <div class="space-y-1">
                  <div class="font-bold text-sm line-clamp-2 group-hover:text-primary transition-colors">{{ task.title
}}</div>
                  <div class="text-xs text-muted-foreground">{{ new Date(task.processed_at).toLocaleTimeString([],
                    { hour: '2-digit', minute: '2-digit' }) }}</div>
                  <div
                    class="inline-flex items-center gap-1.5 text-xs font-bold text-green-600 bg-green-500/10 px-2 py-0.5 rounded-md mt-1">
                    <PlusCircle class="w-3 h-3" />
                    10 XP
                  </div>
                </div>
              </div>
            </div>

            <div v-else class="text-center py-12 text-muted-foreground">
              <div class="inline-flex p-4 rounded-full bg-muted mb-4">
                <ClipboardList class="w-8 h-8" />
              </div>
              <p>No tasks completed yet.</p>
              <p class="text-sm mt-2">Sync TickTick to get started!</p>
            </div>
          </div>
        </div>
      </div>
    </main>

    <LevelUpModal :show="showLevelUp" :level="player?.level || 1" @close="showLevelUp = false" />
    <GatchaAnimation v-if="showGatcha && dropData" :drop="dropData" @close="closeGatcha" />
  </div>
</template>

<style>
@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }

  100% {
    transform: translateX(100%);
  }
}
</style>
