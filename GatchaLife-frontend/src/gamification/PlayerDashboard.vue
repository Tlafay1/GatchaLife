<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import SummonBanner from '@/components/SummonBanner.vue';
import StatCard from '@/components/StatCard.vue';
import LevelUpModal from '@/components/LevelUpModal.vue';
import {
  Coins,
  Sparkles,
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
            class="relative w-full lg:w-[45%] min-h-[400px] lg:min-h-[600px] flex items-center justify-center bg-gradient-to-b from-transparent via-indigo-950/20 to-indigo-950/40 p-6 group/spotlight overflow-visible border-b lg:border-b-0 lg:border-r border-white/5">

            <!-- Ambient Glow behind character -->
            <div
              class="absolute inset-0 bg-radial-gradient from-indigo-500/10 to-transparent opacity-50 pointer-events-none">
            </div>

            <!-- Loading State -->
            <div v-if="isLoading" class="flex flex-col items-center gap-4 text-muted-foreground animate-pulse z-10">
              <div class="relative">
                <div class="absolute inset-0 bg-indigo-500/20 blur-xl rounded-full"></div>
                <Loader2 class="w-10 h-10 animate-spin relative z-10 text-indigo-400" />
              </div>
              <span class="text-xs font-bold tracking-widest uppercase opacity-70">Summoning Companion...</span>
            </div>

            <!-- Error State -->
            <div v-else-if="isError"
              class="relative z-10 text-center text-red-400 p-6 bg-black/60 backdrop-blur-xl rounded-2xl border border-red-500/20 shadow-2xl">
              <p class="font-bold mb-3 text-lg">Connection Lost</p>
              <button @click="refetchTamagotchi()"
                class="px-6 py-2 bg-red-500/20 hover:bg-red-500/40 rounded-lg text-sm font-bold uppercase tracking-wide transition-all hover:scale-105 active:scale-95">Reconnect
                System</button>
            </div>

            <!-- HATCH STATE (No Companion) -->
            <div v-else-if="!tamagotchi" class="text-center relative z-10">
              <button @click="showHatchModal = true"
                class="group relative flex flex-col items-center gap-6 p-10 rounded-3xl hover:bg-white/5 transition-all duration-500 border border-transparent hover:border-white/10 hover:shadow-2xl hover:shadow-indigo-500/10">
                <div
                  class="w-32 h-32 sm:w-40 sm:h-40 flex items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full shadow-[0_0_50px_rgba(124,58,237,0.5)] animate-bounce group-hover:shadow-[0_0_100px_rgba(124,58,237,0.8)] transition-all duration-500">
                  <Sparkles class="w-16 h-16 sm:w-20 sm:h-20 text-white" />
                </div>
                <div>
                  <h3 class="text-3xl font-black text-white mb-2 tracking-tight">Summon Companion</h3>
                  <p class="text-indigo-200 font-medium">Begin your journey</p>
                </div>
              </button>
            </div>

            <!-- COMPANION ACTIVE STATE -->
            <div v-else-if="tamagotchi" class="relative w-full h-full flex flex-col items-center justify-center">

              <!-- Character Aura/Glow based on Mood -->
              <div
                class="absolute inset-0 flex items-center justify-center pointer-events-none transition-opacity duration-1000"
                :class="tamagotchi.mood > 50 ? 'opacity-100' : 'opacity-20'">
                <div class="w-[300px] h-[300px] bg-pink-500/20 rounded-full blur-[100px] animate-pulse"></div>
              </div>

              <!-- Main Character Image (Dynamic Sizing) -->
              <div
                class="relative flex items-center justify-center h-[350px] sm:h-[480px] w-full transition-all duration-500 z-10 group-hover/spotlight:scale-105">
                <img v-if="tamagotchi.character_image" :src="tamagotchi.character_image"
                  class="h-full w-auto object-contain max-w-full drop-shadow-[0_0_25px_rgba(0,0,0,0.5)] animate-in fade-in zoom-in-95 duration-1000 select-none pointer-events-none filter"
                  :class="tamagotchi.mood === 0 ? 'grayscale brightness-50 contrast-125' : ''"
                  alt="My Companion" />
                <div v-else class="text-9xl animate-bounce filter drop-shadow-2xl grayscale opacity-50">🐣</div>
              </div>

              <!-- Settings & Library Buttons (Glassmorphism) -->
              <div class="absolute top-4 left-4 z-20 flex flex-col gap-3">
                <button @click="showSettingsModal = true"
                  class="p-3 rounded-2xl bg-black/20 text-white/70 hover:text-white hover:bg-black/80 backdrop-blur-xl shadow-lg border border-white/10 transition-all hover:scale-110 active:scale-95 group/btn"
                  title="Settings">
                  <Settings class="w-5 h-5 group-hover/btn:rotate-90 transition-transform duration-500" />
                </button>
                <button @click="showImageManager = true"
                  class="p-3 rounded-2xl bg-black/20 text-white/70 hover:text-white hover:bg-black/80 backdrop-blur-xl shadow-lg border border-white/10 transition-all hover:scale-110 active:scale-95"
                  title="Manage Images">
                  <Library class="w-5 h-5" />
                </button>
              </div>

              <!-- DIALOGUE BUBBLE -->
              <div v-if="interactionMessage"
                class="absolute top-[15%] left-1/2 -translate-x-1/2 z-30 animate-in fade-in zoom-in slide-in-from-bottom-2 duration-300 w-max max-w-[90%]">
                <div
                  class="relative bg-white/95 backdrop-blur-sm text-slate-900 px-6 py-3 rounded-2xl shadow-[0_10px_30px_rgba(0,0,0,0.2)] font-bold text-sm min-w-[200px] text-center border-2 border-white/50">
                  <span class="text-base">{{ interactionMessage }}</span>
                  <div
                    class="absolute -bottom-2 left-1/2 -translate-x-1/2 w-4 h-4 bg-white rotate-45 border-r-2 border-b-2 border-white/50">
                  </div>
                </div>
              </div>

              <!-- Name Badge (Floating & Premium) -->
              <div
                class="absolute bottom-8 inset-x-0 mx-auto w-max max-w-[90%] z-20 transition-all duration-300 group-hover/spotlight:-translate-y-2">
                <div
                  class="bg-black/60 backdrop-blur-xl border border-white/10 px-8 py-3 rounded-full shadow-[0_10px_40px_-10px_rgba(0,0,0,0.5)] flex items-center gap-3">
                  <span class="w-2 h-2 rounded-full animate-pulse"
                    :class="tamagotchi.mood > 50 ? 'bg-emerald-400' : (tamagotchi.mood > 20 ? 'bg-yellow-400' : 'bg-red-500')"></span>
                  <span class="font-black text-white tracking-wide text-xl">{{ tamagotchi.name }}</span>
                </div>
              </div>
            </div>

            <!-- DEAD STATE OVERLAY (System Failure Theme) -->
            <div v-if="tamagotchi?.mood === 0"
              class="absolute inset-0 z-40 bg-black/70 backdrop-blur-sm flex flex-col items-center justify-center text-center p-8 transition-all duration-1000">
              <div
                class="w-full max-w-sm p-8 rounded-3xl bg-black/80 border border-red-500/30 shadow-[0_0_60px_rgba(220,38,38,0.2)] relative overflow-hidden">
                <div
                  class="absolute inset-0 bg-[repeating-linear-gradient(45deg,transparent,transparent_10px,rgba(220,38,38,0.05)_10px,rgba(220,38,38,0.05)_20px)] pointer-events-none">
                </div>

                <h2
                  class="text-4xl font-black text-red-500 mb-2 tracking-tighter uppercase drop-shadow-[0_0_10px_rgba(220,38,38,0.5)]">
                  Critial Failure</h2>
                <div class="h-0.5 w-16 bg-red-500/50 mx-auto mb-6"></div>

                <p class="text-red-200/70 mb-8 font-mono text-sm leading-relaxed">
                  Vital signs undetected.<br>Companion data fragmenting.<br>Immediate restoration required.
                </p>

                <button @click="handleResurrect"
                  class="w-full py-4 bg-red-600 hover:bg-red-500 text-white font-bold rounded-xl flex items-center justify-center gap-2 transition-all hover:scale-105 active:scale-95 shadow-[0_0_30px_rgba(220,38,38,0.4)] group uppercase tracking-widest text-sm">
                  <Heart class="w-5 h-5 fill-current group-hover:animate-ping" />
                  <span>Initialize Restore</span>
                  <span class="opacity-60 text-xs ml-1">(1000c)</span>
                </button>
              </div>
            </div>
          </div>

          <!-- RIGHT COLUMN: Dashboard & Stats (55%) -->
          <div
            class="relative flex-1 p-8 sm:p-12 flex flex-col justify-between border-t lg:border-t-0 lg:border-l border-white/5 bg-gradient-to-br from-white/[0.02] to-transparent relative overflow-hidden">







            <!-- Decorative background elements -->
            <div class="absolute top-0 right-0 p-12 opacity-10 pointer-events-none">
              <Sparkles class="w-64 h-64 text-white" />
            </div>

            <!-- Header -->
            <div class="relative z-10 mb-10">
              <div
                class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-xs font-bold uppercase tracking-wider text-emerald-400 mb-4 shadow-[0_0_10px_rgba(16,185,129,0.2)]">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                Connected
              </div>

              <h1 class="text-4xl lg:text-5xl font-black tracking-tight leading-none mb-4">
                Welcome back, <br />
                <span
                  class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 animate-gradient-x">{{
                    player?.user?.username || 'Player' }}</span>
              </h1>

              <p class="text-slate-400 text-sm font-medium max-w-md leading-relaxed">System ready. Tasks synced.
                Completing objectives will increase your synchronization rate.</p>
            </div>

            <!-- Stats & Vitals Grid -->
            <div class="grid gap-6 relative z-10">

              <!-- Level Logic Card -->
              <div
                class="p-6 rounded-2xl bg-black/20 border border-white/5 backdrop-blur-sm hover:bg-black/30 transition-all group relative overflow-hidden">
                <div
                  class="absolute inset-0 bg-gradient-to-r from-indigo-500/10 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700">
                </div>

                <div class="flex justify-between items-end mb-3 relative z-10">
                  <div>
                    <div
class="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">
                      Sync Level</div>
                    <div class="text-4xl font-black text-white tracking-tighter">{{ player?.level || 1 }}</div>
                  </div>
                  <div class="text-right">
                    <span class="text-indigo-400 font-bold text-lg">{{ player?.xp || 0 }}</span>
                    <span class="text-slate-500 text-sm font-medium"> / {{ (player?.level || 1) * 100 }} XP</span>
                  </div>
                </div>

                <!-- Enhanced XP Bar -->
                <div
                  class="h-3 w-full bg-slate-800/50 rounded-full overflow-hidden backdrop-blur-sm border border-white/5 relative z-10">
                  <div
                    class="h-full bg-gradient-to-r from-indigo-600 via-purple-500 to-pink-500 shadow-[0_0_15px_rgba(168,85,247,0.5)] relative overflow-hidden transition-all duration-1000 ease-out"
                    :style="{ width: `${xpPercentage}%` }">
                    <div
                      class="absolute inset-0 bg-gradient-to-r from-transparent via-white/40 to-transparent w-full -translate-x-full animate-[shimmer_2s_infinite]">
                    </div>
                  </div>
                </div>



         



                <div class="mt-3 flex justify-between items-center relative z-10">
                  <div
                    class="px-2 py-1 rounded bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[10px] font-bold uppercase tracking-wider">
                    Luck +{{ Math.min((player?.level || 1) * 0.5, 20).toFixed(1) }}%
                  </div>
                  <span class="text-xs text-slate-500 font-medium">{{ Math.floor(((player?.level || 1) * 100) -
                    (player?.xp || 0)) }} XP to next level</span>
                </div>
              </div>

              <!-- Companion Vitals (if Active) -->
              <div v-if="tamagotchi" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <!-- Mood Card -->
                <div
                  class="p-5 rounded-2xl bg-slate-900/40 border border-white/10 relative overflow-hidden group/stat hover:border-pink-500/30 transition-all">
                  <div class="flex justify-between items-center mb-4">
                    <span
                      class="text-xs font-bold text-slate-400 uppercase tracking-widest group-hover/stat:text-pink-300 transition-colors">Mood</span>
                    <Heart class="w-4 h-4 text-pink-500/50 group-hover/stat:text-pink-400 transition-colors" />
                  </div>

                  <div class="flex items-end gap-2 mb-2">
                    <span class="text-3xl font-black text-white">{{ tamagotchi.mood.toFixed(0) }}</span>
                    <span class="text-sm font-bold text-slate-500 mb-1">/ 100</span>
                  </div>

                  <div class="h-1.5 w-full bg-black/40 rounded-full overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-pink-600 to-pink-400 transition-all duration-1000"
                      :style="{ width: `${tamagotchi.mood}%` }"></div>
                  </div>
                </div>

                <!-- Actions Panel -->
                <div
                  class="p-5 rounded-2xl bg-slate-900/40 border border-white/10 flex flex-col justify-center gap-3 relative overflow-hidden group/panel hover:border-indigo-500/30 transition-all">
                  <div
                    class="absolute inset-0 bg-gradient-to-br from-indigo-500/5 to-purple-500/5 opacity-0 group-hover/panel:opacity-100 transition-opacity">
                  </div>

                  <h3 class="text-[10px] font-bold text-slate-500 uppercase tracking-widest px-1">Interactions</h3>
                  <div class="flex gap-2 relative z-10">
                    <button @click="handleFeed" :disabled="tamagotchi.mood === 0"
                      class="flex-1 py-2 px-3 bg-white/5 hover:bg-white/10 active:bg-white/20 rounded-xl border border-white/5 flex items-center justify-center gap-2 transition-all disabled:opacity-30 disabled:cursor-not-allowed group/btn hover:border-orange-500/30">
                      <Utensils class="w-4 h-4 text-slate-400 group-hover/btn:text-orange-400 transition-colors" />
                      <span class="text-xs font-bold text-slate-300 group-hover/btn:text-white">Feed</span>
                    </button>
                    <button @click="handlePet" :disabled="tamagotchi.mood === 0"
                      class="flex-1 py-2 px-3 bg-white/5 hover:bg-white/10 active:bg-white/20 rounded-xl border border-white/5 flex items-center justify-center gap-2 transition-all disabled:opacity-30 disabled:cursor-not-allowed group/btn hover:border-pink-500/30">
                      <Heart
                        class="w-4 h-4 text-slate-400 group-hover/btn:text-pink-400 transition-colors group-hover/btn:scale-110" />
                      <span class="text-xs font-bold text-slate-300 group-hover/btn:text-white">Pet</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Manual Task & Bottom Actions -->
            <div class="mt-8 relative z-10 pt-6 border-t border-white/5 flex gap-4">
              <button @click="showManualTaskModal = true"
                class="flex-1 py-4 px-6 bg-white/5 hover:bg-white/10 hover:shadow-lg hover:shadow-emerald-500/10 border border-white/10 hover:border-emerald-500/30 rounded-2xl font-bold flex items-center justify-center gap-3 transition-all group w-full">
                <div class="bg-emerald-500/20 p-2 rounded-xl group-hover:scale-110 transition-transform">
                  <PlusCircle class="w-5 h-5 text-emerald-400" />
                </div>
                <span class="text-slate-300 group-hover:text-white font-medium">Add Manual Task</span>
              </button>




       




           
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-12" v-motion-slide-visible-once-bottom>
        <StatCard title="Tasks Completed" :value="stats?.completed_today || 0" :icon="CheckCircle2"
          color="text-emerald-400" bg-gradient="from-emerald-500/10 to-transparent"
          class="bg-slate-900 border-white/10 shadow-lg hover:shadow-emerald-500/10 hover:border-emerald-500/30 transition-all" />

        <StatCard title="Gatcha Coins" :value="player?.gatcha_coins || 0" :icon="Coins" color="text-yellow-400"
          bg-gradient="from-yellow-500/10 to-transparent"
          class="bg-slate-900 border-white/10 shadow-lg hover:shadow-yellow-500/10 hover:border-yellow-500/30 transition-all" />

        <StatCard title="Collection" :value="collection?.length || 0" :icon="Library" color="text-purple-400"
          bg-gradient="from-purple-500/10 to-transparent" clickable @click="$router.push('/collection')"
          class="bg-slate-900 border-white/10 shadow-lg hover:shadow-purple-500/10 hover:border-purple-500/30 transition-all cursor-pointer" />

        <StatCard title="Current Streak" :value="`${stats?.current_streak || 0} Days`" :icon="Flame"
          color="text-orange-400" bg-gradient="from-orange-500/10 to-transparent"
          class="bg-slate-900 border-white/10 shadow-lg hover:shadow-orange-500/10 hover:border-orange-500/30 transition-all" />
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 xl:grid-cols-3 gap-8">

        <!-- Summon Section -->
        <div class="xl:col-span-2 space-y-6" v-motion :initial="{ opacity: 0, x: -20 }"
          :enter="{ opacity: 1, x: 0, transition: { delay: 400 } }">
          <div class="flex items-center justify-between">
            <h2 class="text-2xl font-black tracking-tight text-slate-800 dark:text-white flex items-center gap-2">
              <Sparkles class="w-5 h-5 text-indigo-500" />
              Summon Cards
            </h2>
            <div class="text-sm font-bold text-indigo-600 bg-indigo-50 px-3 py-1 rounded-full border border-indigo-100">
              100
              Coins / Roll</div>
          </div>

          <SummonBanner />
        </div>

        <!-- Recent Activity Feed -->
        <div class="space-y-6" v-motion :initial="{ opacity: 0, x: 20 }"
          :enter="{ opacity: 1, x: 0, transition: { delay: 600 } }">
          <div class="flex items-center justify-between">
            <h2 class="text-2xl font-black tracking-tight text-slate-800 dark:text-white">Recent Activity</h2>
            <router-link to="/history"
              class="text-xs font-bold text-indigo-500 hover:text-indigo-600 uppercase tracking-widest transition-colors">
              View All
            </router-link>
          </div>

          <div
            class="bg-slate-900 border border-white/10 rounded-3xl p-6 shadow-xl min-h-[400px] relative overflow-hidden">
            <!-- Glossy reflection -->
            <div
              class="absolute top-0 right-0 w-full h-full bg-gradient-to-bl from-white/5 to-transparent pointer-events-none">
            </div>

            <div v-if="statsLoading" class="flex justify-center py-8">
              <span class="animate-spin text-muted-foreground">↻</span>
            </div>

            <div v-else-if="stats?.recent_activity?.length" class="space-y-8 relative z-10">
              <!-- Timeline Line -->
              <div class="absolute left-[19px] top-2 bottom-2 w-[2px] bg-white/5"></div>



            <div v-for="task in stats.recent_activity" :key="task.id" class="relative pl-12 group">
                <!-- Timeline Dot -->
                <div
                  class="absolute left-[15px] top-1.5 w-2.5 h-2.5 rounded-full bg-emerald-500 ring-4 ring-black/50 group-hover:scale-150 group-hover:ring-emerald-500/30 transition-all duration-300 z-10">
                </div>

                <div class="space-y-2">
                  <div class="flex flex-col">
                    <div
                      class="font-bold text-sm line-clamp-2 text-slate-200 group-hover:text-white transition-colors duration-300">
                      {{ task.title }}</div>
                    <div class="text-[10px] uppercase tracking-widest font-bold text-slate-600 mt-1">{{ new
                      Date(task.processed_at).toLocaleTimeString([],

 
                    { hour: '2-digit', minute: '2-digit' }) }}</div>
                  </div>



                <div class="flex flex-wrap gap-2">
                    <!-- XP Badge -->
                    <div
                      class="inline-flex items-center gap-1.5 text-[10px] font-bold text-blue-300 bg-blue-500/10 px-2 py-1 rounded border border-blue-500/20">
                      <PlusCircle class="w-3 h-3" />
                      {{ task.xp_gain || '?' }} XP
                    </div>

                    <!-- Coins Badge -->
                    <div
                      class="inline-flex items-center gap-1.5 text-[10px] font-bold text-yellow-300 bg-yellow-500/10 px-2 py-1 rounded border border-yellow-500/20">
                      <Coins class="w-3 h-3" />
                      {{ task.coin_gain || '?' }}
                    </div>

                    <!-- Difficulty Badge -->
                    <div v-if="task.difficulty"
                      class="inline-flex items-center gap-1.5 text-[10px] font-bold px-2 py-1 rounded border capitalize"
                      :class="getDifficultyColor(task.difficulty)">
                      {{ task.difficulty }}
                    </div>

                    <!-- Crit Badge -->
                    <div v-if="task.is_crit"
                      class="inline-flex items-center gap-1.5 text-[10px] font-black text-purple-300 bg-purple-500/10 px-2 py-1 rounded border border-purple-500/20 animate-pulse shadow-[0_0_10px_rgba(168,85,247,0.3)]">
                      <Sparkles class="w-3 h-3" />
                      CRIT!
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-else class="flex flex-col items-center justify-center py-12 text-slate-500 h-full">
              <div class="inline-flex p-4 rounded-full bg-white/5 mb-4 animate-pulse">
                <ClipboardList class="w-8 h-8 opacity-50" />
              </div>
              <p class="font-bold">No tasks completed yet.</p>
              <p class="text-xs mt-2 opacity-50">Sync TickTick to get started!</p>
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

