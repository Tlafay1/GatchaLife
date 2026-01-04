<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import SummonBanner from '@/components/SummonBanner.vue';
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
  Flame,
  X,
  Settings,
  Loader2,
  Heart,
  Utensils
} from 'lucide-vue-next';
import { usePlayerStats, useGatchaRoll, useTickTickStats, useCollection, useManualTask, useTamagotchi, useTamagotchiActions } from '@/lib/api-client';
import TamagotchiHatchModal from './TamagotchiHatchModal.vue';
import TamagotchiSettingsModal from './TamagotchiSettingsModal.vue';
import CompanionImageManager from './CompanionImageManager.vue';

const { data: player, refetch: refetchPlayer } = usePlayerStats();
const { data: stats, isLoading: statsLoading } = useTickTickStats();
const { data: collection } = useCollection();
const { mutate: addManualTask, isPending: isAddingTask } = useManualTask();
const { data: tamagotchi, isLoading, isError, error, refetch: refetchTamagotchi } = useTamagotchi();
const { feed, pet, resurrect } = useTamagotchiActions();

const showLevelUp = ref(false);
const showManualTaskModal = ref(false);
const showHatchModal = ref(false);
const showSettingsModal = ref(false);
const showImageManager = ref(false); // New state

const interactionMessage = ref<string | null>(null);

const manualTaskTitle = ref('');
const manualTaskDifficulty = ref('easy');

// Watch for level up
watch(() => player.value?.level, (newLevel, oldLevel) => {
  if (oldLevel && newLevel && newLevel > oldLevel) {
    showLevelUp.value = true;
  }
});

const handleFeed = async () => {
  if (!tamagotchi.value) return;
  try {
    const result = await feed.mutateAsync(tamagotchi.value.id);
    interactionMessage.value = result.detail;
    setTimeout(() => interactionMessage.value = null, 3000);
  } catch (e: any) {
    interactionMessage.value = e.message;
    setTimeout(() => interactionMessage.value = null, 3000);
  }
};

const handlePet = async () => {
  if (!tamagotchi.value) return;
  try {
    const result = await pet.mutateAsync(tamagotchi.value.id);
    interactionMessage.value = result.detail;
    setTimeout(() => interactionMessage.value = null, 3000);
  } catch (e: any) {
    interactionMessage.value = e.message;
    setTimeout(() => interactionMessage.value = null, 3000);
  }
};

const handleResurrect = async () => {
  if (!tamagotchi.value) return;
  if (confirm("Resurrect companion for 1000 coins?")) {
    try {
      const result = await resurrect.mutateAsync(tamagotchi.value.id);
      interactionMessage.value = result.detail;
      setTimeout(() => interactionMessage.value = null, 3000);
      refetchPlayer(); // Deduct coins
    } catch (e: any) {
      interactionMessage.value = e.message;
      setTimeout(() => interactionMessage.value = null, 4000);
    }
  }
};

const handleManualTaskSubmit = () => {
  if (!manualTaskTitle.value) return;
  
  addManualTask({
    title: manualTaskTitle.value,
    difficulty: manualTaskDifficulty.value
  }, {
    onSuccess: () => {
      showManualTaskModal.value = false;
      manualTaskTitle.value = '';
      manualTaskDifficulty.value = 'easy';
      // Ideally show a success toast here
    }
  });
};

const xpPercentage = computed(() => {
  if (!player.value) return 0;
  const maxXp = player.value.level * 100;
  return Math.min((player.value.xp / maxXp) * 100, 100);
});
const getDifficultyColor = (difficulty: string) => {
  switch (difficulty?.toLowerCase()) {
    case 'extreme': return 'bg-red-500/10 text-red-500 border-red-500/20';
    case 'hard': return 'bg-orange-500/10 text-orange-500 border-orange-500/20';
    case 'medium': return 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20';
    default: return 'bg-green-500/10 text-green-500 border-green-500/20';
  }
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
            class="hidden md:flex p-2 rounded-full hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
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
        class="relative overflow-hidden rounded-3xl bg-slate-900 border border-white/10 shadow-2xl p-0 mb-8 min-h-[450px] animate-in fade-in slide-in-from-top-4 duration-700">
        <!-- Background Gradients -->
        <div class="absolute inset-0 bg-gradient-to-br from-slate-900 via-slate-900 to-indigo-950"></div>
        <div class="absolute top-0 right-0 w-96 h-96 bg-purple-500/20 blur-[100px] rounded-full animate-pulse">
        </div>
        <div class="absolute bottom-0 left-0 w-96 h-96 bg-blue-500/20 blur-[100px] rounded-full"></div>

        <!-- Grid Pattern -->
        <div
          class="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:40px_40px] opacity-20">
        </div>

        <div class="relative z-10 flex flex-col lg:flex-row h-full">

          <!-- LEFT COLUMN: Companion Spotlight (45%) -->
          <div
            class="relative w-full lg:w-[45%] min-h-[400px] flex items-center justify-center bg-gradient-to-r from-black/20 to-transparent p-6 group/spotlight overflow-visible">

            <!-- Loading State -->
            <div v-if="isLoading" class="flex flex-col items-center gap-4 text-muted-foreground animate-pulse">
              <Loader2 class="w-10 h-10 animate-spin" />
              <span>Summoning Companion...</span>
            </div>

            <!-- Error State -->
            <div v-else-if="isError"
              class="text-center text-red-400 p-4 bg-black/40 rounded-xl border border-red-500/20">
              <p class="font-bold mb-2">Connection Lost</p>
              <button @click="refetchTamagotchi()"
                class="px-4 py-2 bg-red-500/20 hover:bg-red-500/40 rounded-lg text-sm transition-colors">Reconnect</button>
            </div>

            <!-- HATCH STATE (No Companion) -->
            <div v-else-if="!tamagotchi" class="text-center">
              <button @click="showHatchModal = true"
                class="group relative flex flex-col items-center gap-6 p-8 rounded-2xl hover:bg-white/5 transition-all duration-500 hover:scale-105">
                <div
                  class="w-24 h-24 sm:w-32 sm:h-32 flex items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full shadow-[0_0_50px_rgba(124,58,237,0.5)] animate-bounce group-hover:shadow-[0_0_80px_rgba(124,58,237,0.7)] transition-shadow">
                  <Sparkles class="w-12 h-12 sm:w-16 sm:h-16 text-white" />
                </div>
                <div>
                  <h3 class="text-2xl font-black text-white mb-2">Summon Companion</h3>
                  <p class="text-indigo-200 text-sm">Click to begin your journey</p>
                </div>
              </button>
            </div>

            <!-- COMPANION ACTIVE STATE -->
            <div v-else-if="tamagotchi" class="relative w-full h-full flex flex-col items-center justify-center">
              <!-- Main Character Image (Full Height) -->
              <div
                class="relative flex items-center justify-center h-[280px] sm:h-[400px] w-full filter drop-shadow-[0_0_15px_rgba(255,255,255,0.1)] hover:drop-shadow-[0_0_30px_rgba(255,255,255,0.3)] transition-all duration-500 z-10">
                <img v-if="tamagotchi.character_image" :src="tamagotchi.character_image"
                  class="h-full w-auto object-contain max-w-full animate-in fade-in zoom-in-95 duration-1000 select-none pointer-events-none"
                  alt="My Companion" />
                <div v-else class="text-9xl animate-bounce filter drop-shadow-2xl">🐣</div>
              </div>

              <!-- Settings & Library Buttons -->
              <div class="absolute top-4 left-4 z-20 flex flex-col gap-2">
                <button @click="showSettingsModal = true"
                  class="p-2 rounded-full bg-black/40 text-black/50 hover:text-white hover:bg-black/60 backdrop-blur-sm shadow-lg border border-white/5 transition-all hover:scale-110 active:scale-95"
                  title="Settings">
                  <Settings class="w-5 h-5" />
                </button>
                <button @click="showImageManager = true"
                  class="p-2 rounded-full bg-black/40 text-black/50 hover:text-white hover:bg-black/60 backdrop-blur-sm shadow-lg border border-white/5 transition-all hover:scale-110 active:scale-95"
                  title="Manage Images">
                  <Library class="w-5 h-5" />
                </button>
              </div>

              <!-- DIALOGUE BUBBLE -->
              <div v-if="interactionMessage"
                class="absolute top-[20%] left-1/2 -translate-x-1/2 z-30 animate-in fade-in zoom-in slide-in-from-bottom-2 duration-300">
                <div
                  class="relative bg-white text-black px-6 py-3 rounded-2xl shadow-xl font-bold text-sm min-w-[200px] text-center">
                  {{ interactionMessage }}
                  <div class="absolute -bottom-2 left-1/2 -translate-x-1/2 w-4 h-4 bg-white rotate-45"></div>
                </div>
              </div>

              <!-- Name Badge (Floating) -->
              <div
                class="absolute bottom-6 inset-x-0 mx-auto w-max max-w-[90%] bg-black/40 backdrop-blur-lg border border-white/10 px-6 py-2 rounded-full text-center shadow-2xl transform translate-y-4 opacity-100 lg:group-hover/spotlight:translate-y-0 lg:group-hover/spotlight:opacity-100 transition-all duration-300 z-20">
                <span class="font-black text-white tracking-wide text-xl">{{ tamagotchi.name }}</span>
              </div>
            </div>

            <!-- DEAD STATE OVERLAY -->
            <div v-if="tamagotchi?.mood === 0"
              class="absolute inset-0 z-40 bg-black/60 flex flex-col items-center justify-center text-center p-8 backdrop-blur-sm/20">
              <h2 class="text-3xl font-black text-red-500 mb-2">COMPANION LOST</h2>
              <p class="text-slate-400 mb-6 max-w-xs">Your companion has faded away due to neglect. Restore them?</p>
              <button @click="handleResurrect"
                class="px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-bold rounded-full flex items-center gap-2 transition-all hover:scale-105 active:scale-95 shadow-[0_0_30px_rgba(220,38,38,0.5)]">
                <Heart class="w-5 h-5 fill-current" />
                Resurrect (1000 Coins)
              </button>
            </div>
          </div>

          <!-- RIGHT COLUMN: Dashboard & Stats (55%) -->
          <div
            class="relative flex-1 p-6 sm:p-10 flex flex-col justify-center border-t lg:border-t-0 lg:border-l border-white/5 bg-white/[0.02]">



            <!-- Welcome Header -->
            <div class="mb-10">
              <div
                class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs font-bold uppercase tracking-wider text-emerald-400 mb-4 shadow-[0_0_10px_rgba(16,185,129,0.2)]">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                Connected
              </div>

              <h1 class="text-4xl lg:text-5xl font-black tracking-tight leading-none mb-2">
                Welcome back, <br />
                <span
                  class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 animate-gradient-x">{{
                    player?.user?.username || 'Player' }}</span>
              </h1>

              <p class="text-slate-400 text-sm">Complete tasks to evolve your companion.</p>
            </div>

            <!-- XP & Level Progress -->
            <div
              class="mb-8 p-6 rounded-2xl bg-white/5 border border-white/10 relative overflow-hidden group hover:bg-white/10 transition-colors duration-500">
              <div
                class="absolute -top-6 -right-6 w-32 h-32 bg-indigo-500/10 rounded-full blur-2xl group-hover:bg-indigo-500/20 transition-all">
              </div>
              <div
                class="absolute top-0 right-0 p-4 opacity-5 font-black text-7xl select-none group-hover:scale-110 transition-transform duration-700">
                LVL {{ player?.level || 1 }}</div>

              <div class="flex justify-between items-end mb-3 relative z-10">
                <div>
                  <div
                    class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1 group-hover:text-indigo-300 transition-colors">
                    Current Level</div>
                  <div class="text-3xl font-black text-white">{{ player?.level || 1 }}</div>
                </div>
                <div class="text-right">
                  <span class="text-indigo-400 font-bold text-lg">{{ player?.xp || 0 }}</span>
                  <span class="text-slate-500 text-sm font-medium"> / {{ (player?.level || 1) * 100 }} XP</span>
                </div>
              </div>

              <!-- XP Bar -->

              <div
                class="h-4 w-full bg-black/40 rounded-full overflow-hidden backdrop-blur-sm border border-white/5 relative z-10">
                <div
                  class="h-full bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 shadow-[0_0_20px_rgba(99,102,241,0.4)] relative overflow-hidden transition-all duration-1000 ease-out"
                  :style="{ width: `${xpPercentage}%` }">
                  <div
                    class="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent w-full -translate-x-full animate-[shimmer_2s_infinite]">
                  </div>
                </div>
              </div>



              <div class="mt-3 text-xs text-slate-400 flex justify-between font-medium">
                <span class="flex items-center gap-1">Luck Bonus: <span
                    class="text-emerald-400 bg-emerald-400/10 px-1.5 py-0.5 rounded text-[10px]">+{{
                      Math.min((player?.level || 1) * 0.5, 20).toFixed(1) }}%</span></span>
                <span>{{ Math.floor(((player?.level || 1) * 100) - (player?.xp || 0)) }} XP to next level</span>
              </div>
            </div>

            <!-- Active Companion Stats (If Active) -->
            <div v-if="tamagotchi"
              class="grid grid-cols-2 gap-4 animate-in fade-in slide-in-from-right-4 duration-700 delay-100">
              <!-- Mood Stat -->
              <div
                class="p-4 rounded-xl bg-slate-900/40 border border-white/10 hover:border-pink-500/30 transition-all group/stat">
                <div class="flex justify-between items-center mb-2">
                  <span
                    class="text-xs font-bold text-slate-400 uppercase group-hover/stat:text-pink-300 transition-colors">Mood</span>
                  <span class="text-sm font-black text-pink-400">{{ tamagotchi.mood.toFixed(0) }}%</span>
                </div>

                <div class="h-2 w-full bg-black/40 rounded-full overflow-hidden">
                  <div class="h-full bg-gradient-to-r from-pink-600 to-pink-400 transition-all duration-1000"
                    :style="{ width: `${tamagotchi.mood}%` }"></div>
                </div>
              </div>

              <!-- Interaction Buttons -->
              <div class="p-4 rounded-xl bg-slate-900/40 border border-white/10 flex flex-col justify-center gap-2">
                <div class="flex gap-2">
                  <button @click="handleFeed" :disabled="tamagotchi.mood === 0"
                    class="flex-1 py-1.5 px-2 bg-white/5 hover:bg-white/10 active:bg-white/20 rounded-lg border border-white/5 flex flex-col items-center justify-center gap-1 transition-all disabled:opacity-50 disabled:cursor-not-allowed group">
                    <Utensils class="w-4 h-4 text-orange-400 group-hover:scale-110 transition-transform" />
                    <span class="text-[10px] font-bold text-slate-300">Feed</span>
                  </button>
                  <button @click="handlePet" :disabled="tamagotchi.mood === 0"
                    class="flex-1 py-1.5 px-2 bg-white/5 hover:bg-white/10 active:bg-white/20 rounded-lg border border-white/5 flex flex-col items-center justify-center gap-1 transition-all disabled:opacity-50 disabled:cursor-not-allowed group">
                    <Heart class="w-4 h-4 text-pink-400 group-hover:scale-110 transition-transform" />
                    <span class="text-[10px] font-bold text-slate-300">Pet</span>
                  </button>
                </div>
              </div>
            </div>









            <!-- Actions Bar -->
            <div class="mt-8 flex flex-col sm:flex-row gap-4">


 
            <button @click="showManualTaskModal = true"
                class="flex-1 py-4 px-6 bg-white/5 hover:bg-white/10 hover:shadow-lg hover:shadow-emerald-500/10 border border-white/10 hover:border-emerald-500/30 rounded-xl font-bold flex items-center justify-center gap-3 transition-all group w-full">
                <div class="bg-emerald-500/20 p-1.5 rounded-lg group-hover:scale-110 transition-transform">
                  <PlusCircle class="w-5 h-5 text-emerald-400" />
                </div>
                <span class="group-hover:text-white text-slate-200">Add Manual Task</span>


 
            </button>







              <div
                class="px-6 py-4 rounded-xl bg-black/20 border border-white/5 flex items-center gap-3 justify-center min-w-[160px]">
                <div class="relative flex h-3 w-3">
                  <span
                    class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>



 
              </div>

                <span class="text-xs font-bold text-slate-400 uppercase tracking-widest">Listening</span>
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

          <SummonBanner />
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

                  <div class="flex flex-wrap gap-2 mt-1">
                    <!-- XP Badge -->
                    <div
                      class="inline-flex items-center gap-1.5 text-xs font-bold text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded-md border border-blue-500/20">
                      <PlusCircle class="w-3 h-3" />
                      {{ task.xp_gain || '?' }} XP
                    </div>

                    <!-- Coins Badge -->
                    <div
                      class="inline-flex items-center gap-1.5 text-xs font-bold text-yellow-500 bg-yellow-500/10 px-2 py-0.5 rounded-md border border-yellow-500/20">
                      <Coins class="w-3 h-3" />
                      {{ task.coin_gain || '?' }}
                    </div>

                    <!-- Difficulty Badge -->
                    <div v-if="task.difficulty"
                      class="inline-flex items-center gap-1.5 text-xs font-bold px-2 py-0.5 rounded-md border capitalize"
                      :class="getDifficultyColor(task.difficulty)">
                      {{ task.difficulty }}
                    </div>

                    <!-- Crit Badge -->
                    <div v-if="task.is_crit"
                      class="inline-flex items-center gap-1.5 text-xs font-black text-purple-500 bg-purple-500/10 px-2 py-0.5 rounded-md border border-purple-500/20 animate-pulse">
                      <Sparkles class="w-3 h-3" />
                      CRIT!
                    </div>
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

            <div class="mt-6 pt-4 border-t border-border text-center">
              <router-link to="/history" class="text-sm font-bold text-primary hover:underline">
                View Full History →
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </main>
    
    <!-- Manual Task Modal -->
    <Teleport to="body">
      <div v-if="showManualTaskModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm px-4">
        <div class="bg-card border border-border rounded-xl shadow-2xl max-w-md w-full p-6 animate-in fade-in zoom-in-95 duration-200">
          <div class="flex justify-between items-center mb-6">
            <h3 class="text-xl font-bold">Add Manual Task</h3>
            <button @click="showManualTaskModal = false" class="text-muted-foreground hover:text-foreground">
              <X class="w-5 h-5" />
            </button>
          </div>
          
          <div class="space-y-4">
            <div>
              <label class="text-sm font-bold mb-1 block">Task Title</label>
              <input v-model="manualTaskTitle" type="text" placeholder="What did you accomplish?"
                class="w-full px-3 py-2 bg-background border border-input rounded-md focus:ring-2 focus:ring-primary focus:outline-none"
                @keyup.enter="handleManualTaskSubmit"
                 />
            </div>
            
            <div>
              <label class="text-sm font-bold mb-1 block">Difficulty</label>
              <div class="grid grid-cols-4 gap-2">
                 <button v-for="dif in ['easy', 'medium', 'hard', 'extreme']" :key="dif"
                    @click="manualTaskDifficulty = dif"
                    class="px-2 py-2 rounded-md border text-xs font-bold uppercase transition-colors"
                    :class="manualTaskDifficulty === dif ? getDifficultyColor(dif) + ' ring-2 ring-primary ring-offset-2 ring-offset-background' : 'border-border bg-secondary/50 text-muted-foreground hover:bg-secondary'">
                    {{ dif }}
                 </button>
              </div>
            </div>
            
            <button @click="handleManualTaskSubmit" :disabled="!manualTaskTitle || isAddingTask"
              class="w-full py-3 bg-primary hover:bg-primary/90 text-primary-foreground rounded-lg font-bold flex items-center justify-center gap-2 mt-2 disabled:opacity-50">
              <span v-if="isAddingTask" class="animate-spin text-xl">⟳</span>
              <span v-else>Complete Task</span>
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <LevelUpModal :show="showLevelUp" :level="player?.level || 1" @close="showLevelUp = false" />

    <TamagotchiHatchModal :show="showHatchModal" @close="showHatchModal = false" />
    <TamagotchiSettingsModal v-if="tamagotchi" :show="showSettingsModal" :tamagotchi="tamagotchi"
      @close="showSettingsModal = false" />

    <CompanionImageManager v-if="tamagotchi && showImageManager" :show="showImageManager"
      :character-id="tamagotchi.character_id" :character-name="tamagotchi.character_name || tamagotchi.name"
      @close="showImageManager = false" />


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

