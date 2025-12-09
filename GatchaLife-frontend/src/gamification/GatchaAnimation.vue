<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';

const props = defineProps<{
  drops: Array<{
    card: {
      rarity_name: string;
      image_url?: string;
      character_variant_name: string;
      style_name: string;
      theme_name: string;
    };
    is_new: boolean;
  }>;
}>();

const emit = defineEmits(['close']);

// Steps: 'summoning', 'revealing', 'summary'
const step = ref('summoning');
const currentCardIndex = ref(0);
const isCardRevealed = ref(false);

const currentCard = computed(() => {
  if (currentCardIndex.value >= 0 && currentCardIndex.value < props.drops.length) {
    return props.drops[currentCardIndex.value];
  }
  return null;
});

onMounted(() => {
  setTimeout(() => {
    step.value = 'revealing';
  }, 2000); // 2 seconds of summoning animation
});

const handleInteraction = () => {
  if (step.value === 'summoning') return;

  if (step.value === 'revealing') {
    if (!isCardRevealed.value) {
      // Reveal current card
      isCardRevealed.value = true;
    } else {
      // Move to next card
      if (currentCardIndex.value < props.drops.length - 1) {
        currentCardIndex.value++;
        isCardRevealed.value = false;
      } else {
        // Done showing all cards
        step.value = 'summary';
      }
    }
  }
};

const rarityColor = (rarity: string) => {
  switch (rarity?.toLowerCase()) {
    case 'common': return 'text-gray-400 border-gray-400 shadow-gray-400/20';
    case 'rare': return 'text-blue-400 border-blue-400 shadow-blue-400/20';
    case 'epic': return 'text-purple-400 border-purple-400 shadow-purple-400/20';
    case 'legendary': return 'text-yellow-400 border-yellow-400 shadow-yellow-400/20';
    default: return 'text-white border-white';
  }
};
</script>

<template>
  <Teleport to="body">
    <div class="fixed inset-0 z-[100] flex flex-col items-center justify-center bg-black overflow-hidden"
      @click="handleInteraction">

      <!-- Ambient Background -->
      <div class="absolute inset-0 z-0">
        <div
          class="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-indigo-900/40 via-black to-black animate-pulse-slow">
        </div>
        <!-- Stars/Particles -->
        <div class="stars absolute inset-0 opacity-50"></div>
        <div class="stars2 absolute inset-0 opacity-30"></div>
      </div>

      <!-- Summoning Animation -->
      <div v-if="step === 'summoning'"
        class="relative z-10 flex flex-col items-center gap-8 animate-in fade-in duration-1000">
        <div class="relative">
          <div class="absolute inset-0 bg-blue-500 blur-3xl opacity-20 animate-pulse"></div>
          <div
            class="w-48 h-48 rounded-full border-4 border-blue-500/30 border-t-blue-400 animate-spin shadow-[0_0_50px_rgba(59,130,246,0.5)]">
          </div>
          <div class="absolute inset-0 flex items-center justify-center">
            <div class="w-32 h-32 bg-blue-500/10 rounded-full animate-ping"></div>
          </div>
        </div>
        <div
          class="text-4xl font-black text-white tracking-[0.5em] uppercase text-transparent bg-clip-text bg-gradient-to-r from-blue-200 to-indigo-200 animate-pulse">
          Summoning
        </div>
      </div>

      <!-- Active Reveal View -->
      <div v-else-if="step === 'revealing' && currentCard"
        class="relative z-10 flex flex-col items-center justify-center w-full h-full p-6">

        <Transition name="card-zoom" mode="out-in">
          <div :key="currentCardIndex" class="relative w-full max-w-md aspect-[2/3] perspective-1000">
            <!-- Spotlight -->
            <div
              class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[200%] h-[200%] bg-gradient-to-r from-indigo-500/20 to-purple-500/20 blur-3xl rounded-full pointer-events-none">
            </div>

            <!-- Card Container -->
            <div class="w-full h-full transition-all duration-700 preserve-3d relative cursor-pointer"
              :class="{ 'rotate-y-180': isCardRevealed }">
              <!-- Card Back -->
              <div class="absolute inset-0 backface-hidden">
                <div
                  class="w-full h-full bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 rounded-3xl border border-indigo-500/50 flex items-center justify-center shadow-[0_0_50px_rgba(79,70,229,0.3)] relative overflow-hidden group hover:scale-[1.02] transition-transform duration-300">
                  <!-- Pattern -->

                  <!-- Glowing Orb -->
                  <div class="w-32 h-32 rounded-full bg-indigo-500/20 blur-xl animate-pulse absolute"></div>
                  <div
                    class="w-40 h-40 border border-indigo-400/30 rounded-full animate-[spin_10s_linear_infinite] absolute">
                  </div>
                  <div
                    class="w-28 h-28 border border-purple-400/30 rounded-full animate-[spin_7s_linear_infinite_reverse] absolute">
                  </div>

                  <div
                    class="absolute bottom-12 text-indigo-200 font-bold tracking-[0.3em] text-sm animate-bounce uppercase">
                    Tap to Reveal
                  </div>
                </div>
              </div>

              <!-- Card Front -->
              <div class="absolute inset-0 backface-hidden rotate-y-180">
                <div
                  class="w-full h-full bg-gray-900 rounded-3xl border border-white/10 shadow-[0_0_100px_rgba(0,0,0,0.8)] overflow-hidden flex flex-col relative"
                  :class="rarityColor(currentCard?.card.rarity_name || '')">
                  <!-- Glow effect matching rarity -->
                  <div
                    class="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-black pointer-events-none z-10">
                  </div>

                  <!-- Image -->
                  <img v-if="currentCard?.card.image_url" :src="currentCard?.card.image_url"
                    class="absolute inset-0 w-full h-full object-cover z-0 transition-transform duration-1000 hover:scale-110" />

                  <!-- New Badge -->
                  <div v-if="currentCard?.is_new"
                    class="absolute top-6 right-6 z-20 bg-yellow-400 text-black text-sm font-black px-4 py-1.5 rounded-full shadow-[0_0_20px_rgba(250,204,21,0.5)] animate-bounce">
                    NEW
                  </div>

                  <!-- Content at bottom -->
                  <div class="mt-auto p-10 z-20 text-center space-y-4">
                    <div
                      class="inline-block px-3 py-1 rounded bg-black/50 backdrop-blur border border-white/20 text-xs font-bold uppercase tracking-[0.2em] text-white/80">
                      {{ currentCard?.card.rarity_name }}
                    </div>
                    <h2
                      class="text-5xl font-black text-white leading-none drop-shadow-[0_4px_4px_rgba(0,0,0,0.8)] tracking-tight">
                      {{ currentCard?.card.character_variant_name }}
                    </h2>
                    <div class="flex items-center justify-center gap-2 text-base font-medium text-gray-300">
                      <span>{{ currentCard?.card.style_name }}</span>
                      <span class="w-1 h-1 rounded-full bg-gray-500"></span>
                      <span>{{ currentCard?.card.theme_name }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Transition>

        <!-- Progress Dots -->
        <div class="absolute bottom-10 flex gap-4">
          <div v-for="(_, idx) in drops" :key="idx"
            class="w-3 h-3 rounded-full transition-all duration-500 border border-white/20"
            :class="idx === currentCardIndex ? 'bg-white scale-125 shadow-[0_0_10px_white]' : (idx < currentCardIndex ? 'bg-indigo-500 border-indigo-500' : 'bg-transparent')">
          </div>
        </div>
      </div>


      <!-- Summary Grid -->
      <div v-else-if="step === 'summary'"
        class="relative z-10 w-full max-w-7xl p-6 flex flex-col items-center justify-center h-full animate-in fade-in duration-500">

        <h2 class="text-4xl md:text-6xl font-black text-white mb-12 tracking-tight drop-shadow-2xl">
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-300 to-purple-300">Discovery
            Complete</span>
        </h2>

        <div class="flex flex-wrap justify-center gap-6 w-full items-center mb-12">
          <div 
v-for="(drop, index) in drops" :key="index"
            class="relative animate-in zoom-in-50 duration-500 fill-mode-backwards"
            :style="{ animationDelay: `${index * 150}ms` }">
            <div
              class="relative w-32 md:w-48 aspect-[2/3] bg-gray-900 rounded-2xl border border-white/10 shadow-2xl overflow-hidden flex flex-col group hover:-translate-y-2 transition-transform duration-300"
              :class="rarityColor(drop.card?.rarity_name)">
              <!-- Image -->
              <div class="flex-1 bg-gray-900 relative">
                <img 
v-if="drop.card?.image_url" :src="drop.card.image_url"
                  class="absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" />

                <div v-if="drop.is_new"
                  class="absolute top-2 right-2 bg-yellow-400 text-black text-[10px] font-black px-2 py-0.5 rounded-full shadow-lg">
                  NEW
                </div>
              </div>

              <div class="p-3 bg-black/90 backdrop-blur-xl border-t border-white/10">
                <h3 class="text-sm font-bold text-white leading-tight truncate">{{ drop.card?.character_variant_name }}
                </h3>
                <div class="text-[10px] text-gray-400 truncate mt-1">{{ drop.card?.rarity_name }}</div>
              </div>
            </div>
          </div>
        </div>

        <button @click.stop="emit('close')"
          class="group relative px-12 py-5 bg-white text-black font-black text-xl rounded-full transition-all hover:scale-105 active:scale-95 shadow-[0_0_30px_rgba(255,255,255,0.3)] hover:shadow-[0_0_50px_rgba(255,255,255,0.5)]">
          <span class="relative z-10">ACCEPT REWARDS</span>
          <div
            class="absolute inset-0 rounded-full bg-gradient-to-r from-indigo-500 via-purple-500 to-indigo-500 opacity-0 group-hover:opacity-10 transition-opacity">
          </div>
        </button>
      </div>

    </div>
  </Teleport>
</template>

<style scoped>
.perspective-1000 {
  perspective: 1000px;
}

.preserve-3d {
  transform-style: preserve-3d;
}

.backface-hidden {
  backface-visibility: hidden;
}

.rotate-y-180 {
  transform: rotateY(180deg);
}

/* Card Zoom Transition */
.card-zoom-enter-active,
.card-zoom-leave-active {
  transition: all 0.5s cubic-bezier(0.19, 1, 0.22, 1);
}

.card-zoom-enter-from {
  opacity: 0;
  transform: scale(0.8) translateY(50px);
}

.card-zoom-leave-to {
  opacity: 0;
  transform: scale(1.2) translateY(-50px);
}

/* Star field placeholder animation */
.stars {
  background-image:
    radial-gradient(1px 1px at 25px 5px, white, transparent),
    radial-gradient(1px 1px at 50px 25px, white, transparent),
    radial-gradient(1px 1px at 125px 20px, white, transparent),
    radial-gradient(1.5px 1.5px at 50% 50%, white, transparent);
  background-size: 250px 250px;
  animation: stars-move 100s linear infinite;
}

.stars2 {
  background-image:
    radial-gradient(2px 2px at 15px 15px, white, transparent),
    radial-gradient(2px 2px at 100px 50px, white, transparent);
  background-size: 150px 150px;
  animation: stars-move 50s linear infinite;
}

@keyframes stars-move {
  from {
    background-position: 0 0;
  }

  to {
    background-position: 0 1000px;
  }
}

.animate-pulse-slow {
  animation: pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
