<script setup lang="ts">
import { ref, computed } from 'vue';
import { useTaskHistory, useProgressionStats } from '@/lib/api-client';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line } from 'vue-chartjs';
import { Coins, PlusCircle, Sparkles, Calendar, ArrowLeft } from 'lucide-vue-next';
import { Button } from '@/components/ui/button';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const page = ref(1);
const { data: history, isLoading: historyLoading } = useTaskHistory(page.value);
const { data: progression, isLoading: progressionLoading } = useProgressionStats();

const getDifficultyColor = (difficulty: string) => {
  switch (difficulty?.toLowerCase()) {
    case 'extreme': return 'bg-red-500/10 text-red-500 border-red-500/20';
    case 'hard': return 'bg-orange-500/10 text-orange-500 border-orange-500/20';
    case 'medium': return 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20';
    default: return 'bg-green-500/10 text-green-500 border-green-500/20';
  }
};

interface DailyStat {
  date: string;
  total_xp: number;
  total_coins: number;
}

const chartData = computed(() => {
  if (!progression.value) return { labels: [], datasets: [] };
  
  const labels = progression.value.map((p: DailyStat) => new Date(p.date).toLocaleDateString(undefined, { month: 'short', day: 'numeric' }));
  const xpData = progression.value.map((p: DailyStat) => p.total_xp);
  const coinsData = progression.value.map((p: DailyStat) => p.total_coins);

  return {
    labels,
    datasets: [
      {
        label: 'XP Earned',
        backgroundColor: 'rgba(59, 130, 246, 0.2)',
        borderColor: '#3b82f6',
        data: xpData,
        fill: true,
        tension: 0.4
      },
      {
        label: 'Coins Earned',
        backgroundColor: 'rgba(234, 179, 8, 0.2)',
        borderColor: '#eab308',
        data: coinsData,
        fill: true,
        tension: 0.4
      }
    ]
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: { color: '#94a3b8' }
    }
  },
  scales: {
    y: {
      grid: { color: '#334155' },
      ticks: { color: '#94a3b8' }
    },
    x: {
      grid: { color: '#334155' },
      ticks: { color: '#94a3b8' }
    }
  }
};
</script>

<template>
  <div class="min-h-screen bg-background text-foreground p-4 md:p-8 font-sans">
    <div class="max-w-6xl mx-auto space-y-8">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-4">
          <router-link to="/" class="hidden md:block">
            <Button variant="ghost" size="icon">
              <ArrowLeft class="w-5 h-5" />
            </Button>
          </router-link>
          <h1 class="text-3xl font-bold">Progression History</h1>
        </div>
      </div>

      <!-- Chart Section -->
      <div class="bg-card border border-border rounded-xl p-6 shadow-sm h-[400px]">
        <h2 class="text-xl font-bold mb-4">Last 30 Days</h2>
        <div v-if="progressionLoading" class="h-full flex items-center justify-center">
          <span class="animate-spin text-muted-foreground">↻</span>
        </div>
        <Line v-else :data="chartData" :options="chartOptions" />
      </div>

      <!-- History List -->
      <div class="space-y-4">
        <h2 class="text-xl font-bold">Task History</h2>

        <div v-if="historyLoading" class="text-center py-12 text-muted-foreground">
          Loading history...
        </div>

        <div v-else class="space-y-4">
          <div v-for="task in history?.results" :key="task.id"
            class="bg-card border border-border rounded-xl p-4 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:border-primary/50 transition-colors group">

            <div class="space-y-1">
              <div class="font-bold text-lg group-hover:text-primary transition-colors">{{ task.title || 'Unknown Task'
                }}</div>
              <div class="flex items-center gap-2 text-xs text-muted-foreground">
                <Calendar class="w-3 h-3" />
                {{ new Date(task.processed_at).toLocaleString() }}
              </div>
            </div>

            <div class="flex flex-wrap items-center gap-3">
              <!-- Breakdown Tooltip Wrapper -->
              <div class="group/tooltip relative">
                <div class="flex flex-wrap gap-2 cursor-help">
                  <!-- XP Badge -->
                  <div
                    class="inline-flex items-center gap-1.5 text-sm font-bold text-blue-400 bg-blue-500/10 px-3 py-1 rounded-md border border-blue-500/20">
                    <PlusCircle class="w-4 h-4" />
                    {{ task.xp_gain }} XP
                  </div>

                  <!-- Coins Badge -->
                  <div
                    class="inline-flex items-center gap-1.5 text-sm font-bold text-yellow-500 bg-yellow-500/10 px-3 py-1 rounded-md border border-yellow-500/20">
                    <Coins class="w-4 h-4" />
                    {{ task.coin_gain }}
                  </div>

                  <!-- Difficulty Badge -->
                  <div class="inline-flex items-center gap-1.5 text-sm font-bold px-3 py-1 rounded-md border capitalize"
                    :class="getDifficultyColor(task.difficulty)">
                    {{ task.difficulty }}
                  </div>

                  <!-- Crit Badge -->
                  <div v-if="task.is_crit"
                    class="inline-flex items-center gap-1.5 text-sm font-black text-purple-500 bg-purple-500/10 px-3 py-1 rounded-md border border-purple-500/20">
                    <Sparkles class="w-4 h-4" />
                    CRIT!
                  </div>
                </div>

                <!-- Detailed Breakdown Tooltip -->
                <div
                  class="absolute bottom-full right-0 mb-2 w-64 p-3 bg-popover text-popover-foreground text-xs rounded-lg border border-border shadow-xl opacity-0 group-hover/tooltip:opacity-100 transition-opacity pointer-events-none z-50">
                  <div class="font-bold mb-2 border-b border-border/50 pb-1">Reward Breakdown</div>
                  <div class="grid grid-cols-2 gap-1">
                    <span class="text-muted-foreground">Base Reward:</span>
                    <span class="text-right">{{ task.base_reward }}</span>

                    <span class="text-muted-foreground">Difficulty:</span>
                    <span class="text-right capitalize">{{ task.difficulty }} (x{{ task.difficulty === 'extreme' ? 3 :
                      task.difficulty === 'hard' ? 2 : task.difficulty === 'medium' ? 1.5 : 1 }})</span>

                    <span class="text-muted-foreground">Streak Bonus:</span>
                    <span class="text-right">x{{ task.streak_multiplier.toFixed(2) }}</span>

                    <span v-if="task.is_crit" class="text-purple-400 font-bold">Crit Multiplier:</span>
                    <span v-if="task.is_crit" class="text-right text-purple-400 font-bold">x{{ task.crit_multiplier
                      }}</span>

                    <span v-if="task.daily_bonus > 0" class="text-green-400">Daily Bonus:</span>
                    <span v-if="task.daily_bonus > 0" class="text-right text-green-400">+{{ task.daily_bonus }}</span>

                    <div class="col-span-2 border-t border-border/50 mt-1 pt-1 flex justify-between font-bold">
                      <span>Total Coins:</span>
                      <span class="text-yellow-500">{{ task.coin_gain }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination (Simple) -->
        <div class="flex justify-center gap-2 mt-8">
          <Button :disabled="page <= 1" @click="page--">Previous</Button>
          <span class="py-2 px-4 bg-muted rounded-md font-mono">{{ page }}</span>
          <Button :disabled="!history?.results?.length || history.results.length < 20" @click="page++">Next</Button>
        </div>
      </div>
    </div>
  </div>
</template>
