<script setup lang="ts">
import { ref } from 'vue';
import { useCreateTamagotchi, useCharacters } from '@/lib/api-client';
import { Sparkles, Loader2 } from 'lucide-vue-next';

defineProps<{
  show: boolean;
}>();

const emit = defineEmits(['close']);

const selectedCharacterId = ref<number | null>(null);
const { mutate: hatch, isPending } = useCreateTamagotchi();
const { data: characters, isLoading: isLoadingCharacters } = useCharacters();

interface Character {
    id: number;
    name: string;
    identity_face_image: string | null;
}

const handleHatch = () => {
  if (!selectedCharacterId.value) return;
  hatch({ character_id: selectedCharacterId.value }, {
    onSuccess: () => {
      emit('close');
      selectedCharacterId.value = null;
    }
  });
};

const getCharacterImage = (char: any) => {
    // Assuming backend provides identity_face_image URL directly or relative
    return char.identity_face_image || '';
};
</script>

<template>
  <Teleport to="body">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm px-4">
      <div 
        class="bg-card w border border-border rounded-xl shadow-2xl max-w-2xl w-full p-6 text-center animate-in fade-in zoom-in-95 duration-300 relative overflow-hidden flex flex-col max-h-[90vh]"
      >
        <!-- Background Glow -->
        <div class="absolute top-0 left-1/2 -translate-x-1/2 w-48 h-48 bg-primary/20 blur-3xl -z-10"></div>

        <div class="flex-none mb-6">
             <div class="mx-auto w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mb-4 animate-bounce">
              <Sparkles class="w-8 h-8 text-primary" />
            </div>
            <h2 class="text-2xl font-black tracking-tight mb-2">Select Your Companion</h2>
            <p class="text-sm text-muted-foreground">
              Choose a character to be your digital partner.
            </p>
        </div>

        <div class="flex-1 overflow-y-auto min-h-0 mb-6 pr-2 custom-scrollbar">
             <div v-if="isLoadingCharacters" class="flex justify-center py-12">
                 <Loader2 class="w-8 h-8 animate-spin text-muted-foreground" />
             </div>
             
             <div v-else-if="characters" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                 <button 
                    v-for="char in characters" 
                    :key="char.id"
                    @click="selectedCharacterId = char.id"
                    class="group relative aspect-square rounded-xl overflow-hidden border-2 transition-all"
                    :class="selectedCharacterId === char.id ? 'border-primary ring-2 ring-primary/50' : 'border-transparent hover:border-white/20'"
                 >
                    <img v-if="char.identity_face_image" :src="char.identity_face_image" class="w-full h-full object-cover transition-transform group-hover:scale-110" />
                    <div v-else class="w-full h-full bg-secondary flex items-center justify-center text-2xl">
                        ?
                    </div>
                    
                    <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent flex items-end p-2 opacity-100">
                        <span class="text-xs font-bold text-white truncate w-full text-center">{{ char.name }}</span>
                    </div>
                 </button>
             </div>
             <p v-else class="text-muted-foreground">No characters found in the studio.</p>
        </div>

        <div class="flex-none space-y-3">
             <button 
            @click="handleHatch"
            :disabled="!selectedCharacterId || isPending"
            class="w-full py-3 bg-primary hover:bg-primary/90 text-primary-foreground font-bold rounded-xl flex items-center justify-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
          >
            <span v-if="isPending" class="animate-spin text-xl">⟳</span>
            <span v-else class="flex items-center gap-2">
              Hatch Companion <Sparkles class="w-4 h-4 group-hover:rotate-12 transition-transform" />
            </span>
          </button>
        
            <button @click="$emit('close')" class="text-xs font-bold text-muted-foreground hover:text-foreground transition-colors">
            Cancel
            </button>
        </div>

      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
}
</style>
