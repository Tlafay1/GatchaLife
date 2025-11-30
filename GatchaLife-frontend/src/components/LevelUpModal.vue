<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps<{
  show: boolean;
  level: number;
}>();

const emit = defineEmits(['close']);

const showContent = ref(false);

watch(() => props.show, (newVal) => {
  if (newVal) {
    setTimeout(() => {
      showContent.value = true;
    }, 100);
  } else {
    showContent.value = false;
  }
});
</script>

<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <!-- Backdrop -->
    <div 
      class="absolute inset-0 bg-black/80 backdrop-blur-sm animate-in fade-in duration-300"
      @click="emit('close')"
    ></div>

    <!-- Content -->
    <div 
      class="relative z-10 w-full max-w-md transform overflow-hidden rounded-3xl bg-gradient-to-b from-slate-900 to-slate-950 p-1 text-center shadow-2xl transition-all animate-in zoom-in-95 duration-300 border border-yellow-500/30"
    >
      <div class="bg-slate-950/50 rounded-[22px] p-8 relative overflow-hidden">
        <!-- Shine effect -->
        <div class="absolute inset-0 bg-gradient-to-tr from-yellow-500/10 via-transparent to-transparent pointer-events-none"></div>
        
        <div class="relative z-10 flex flex-col items-center">
          <div class="mb-6 relative">
            <div class="absolute inset-0 bg-yellow-500 blur-3xl opacity-20 animate-pulse"></div>
            <span class="i-lucide-crown text-6xl text-yellow-400 animate-bounce"></span>
          </div>
          
          <h2 class="text-3xl font-black text-white mb-2 tracking-tight">LEVEL UP!</h2>
          <p class="text-slate-400 mb-8">You are now level</p>
          
          <div class="text-8xl font-black text-transparent bg-clip-text bg-gradient-to-b from-yellow-300 to-yellow-600 mb-8 drop-shadow-2xl">
            {{ level }}
          </div>
          
          <div class="grid grid-cols-2 gap-4 w-full mb-8">
             <div class="bg-slate-900/80 p-4 rounded-xl border border-white/5">
               <div class="text-xs text-slate-500 uppercase font-bold mb-1">Bonus Coins</div>
               <div class="text-xl font-bold text-yellow-400">+50</div>
             </div>
             <div class="bg-slate-900/80 p-4 rounded-xl border border-white/5">
               <div class="text-xs text-slate-500 uppercase font-bold mb-1">Max XP</div>
               <div class="text-xl font-bold text-blue-400">Increased</div>
             </div>
          </div>

          <button 
            @click="emit('close')"
            class="w-full py-4 bg-gradient-to-r from-yellow-500 to-yellow-600 hover:from-yellow-400 hover:to-yellow-500 text-black font-black text-lg rounded-xl shadow-lg shadow-yellow-900/20 transition-all hover:scale-[1.02] active:scale-[0.98]"
          >
            AWESOME!
          </button>
        </div>
      </div>
    </div>
    
    <!-- Confetti (CSS only implementation or placeholder) -->
    <div class="fixed inset-0 pointer-events-none overflow-hidden" v-if="show">
        <div v-for="i in 20" :key="i" class="confetti" :style="{ 
            left: Math.random() * 100 + '%',
            animationDelay: Math.random() * 2 + 's',
            backgroundColor: ['#fbbf24', '#3b82f6', '#ef4444', '#10b981'][Math.floor(Math.random() * 4)]
        }"></div>
    </div>
  </div>
</template>

<style scoped>
.confetti {
  position: absolute;
  top: -10px;
  width: 10px;
  height: 10px;
  border-radius: 2px;
  animation: fall 3s linear infinite;
}

@keyframes fall {
  0% { transform: translateY(0) rotate(0deg); opacity: 1; }
  100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
}
</style>
