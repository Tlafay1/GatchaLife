<script setup lang="ts">
import { ref } from 'vue';
import { useCompanionImages, useUploadCompanionImage, useDeleteCompanionImage } from '@/lib/api-client';
import { Upload, X, Loader2, ImagePlus, Trash2 } from 'lucide-vue-next';

const props = defineProps<{
  show: boolean;
  characterId: number;
  characterName: string;
}>();

const emit = defineEmits(['close']);

const COMPANION_STATES = [
  { value: 'EXTREMELY_HAPPY', label: 'Extremely Happy (80-100%)' },
  { value: 'HAPPY', label: 'Happy (60-80%)' },
  { value: 'NEUTRAL', label: 'Neutral (40-60%)' },
  { value: 'POUTING', label: 'Pouting (20-40%)' },
  { value: 'DISTRESSED', label: 'Very Distressed (1-20%)' },
  { value: 'DEAD', label: 'Dead (0%)' },
  { value: 'SLEEPING', label: 'Sleeping' },
];

const selectedState = ref(COMPANION_STATES[0].value);
const selectedFile = ref<File | null>(null);

const { data: images, isLoading } = useCompanionImages(props.characterId);
const { mutate: uploadImage, isPending: isUploading } = useUploadCompanionImage();
const { mutate: deleteImage, isPending: isDeleting } = useDeleteCompanionImage();
const deletingId = ref<number | null>(null);

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    selectedFile.value = target.files[0];
  }
};

const handleUpload = () => {
    if (!selectedFile.value) return;

    const formData = new FormData();
    formData.append('character', props.characterId.toString());
    formData.append('image', selectedFile.value);
    formData.append('state', selectedState.value);

    uploadImage(formData, {
        onSuccess: () => {
            selectedFile.value = null;
        }
    });
};

const handleDelete = (id: number) => {
    if (confirm('Are you sure you want to delete this appearance?')) {
        deletingId.value = id;
        deleteImage(id, {
            onSettled: () => {
                deletingId.value = null;
            }
        });
    }
};

const getStateLabel = (stateValue: string) => {
    return COMPANION_STATES.find(s => s.value === stateValue)?.label || stateValue;
};
</script>

<template>
  <Teleport to="body">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm px-4">
      <div 
        class="bg-card w border border-border rounded-xl shadow-2xl max-w-2xl w-full p-6 animate-in fade-in zoom-in-95 duration-300 relative overflow-hidden flex flex-col max-h-[90vh]"
      >
        <button @click="$emit('close')" class="absolute top-4 right-4 text-muted-foreground hover:text-white">
            <X class="w-6 h-6" />
        </button>

        <h2 class="text-2xl font-black tracking-tight mb-2">Manage Appearance: {{ characterName }}</h2>
        <p class="text-sm text-muted-foreground mb-6">
            Upload images triggered by specific mood states.
        </p>

        <div class="flex-1 overflow-y-auto min-h-0 mb-6 pr-2 custom-scrollbar">
            
            <!-- Upload Section -->
            <div class="bg-white/5 p-4 rounded-xl border border-white/10 mb-6">
                <h3 class="font-bold text-lg mb-4 flex items-center gap-2">
                    <ImagePlus class="w-5 h-5 text-indigo-400" /> 
                    Add New State
                </h3>
                
                <div class="space-y-4">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="space-y-2">
                            <label class="text-xs uppercase font-bold text-slate-400">Target State</label>
                            <select v-model="selectedState" class="w-full bg-black/20 border border-white/10 rounded px-3 py-2 text-white font-medium focus:ring-2 focus:ring-indigo-500 outline-none">
                                <option v-for="state in COMPANION_STATES" :key="state.value" :value="state.value" class="bg-slate-800">
                                    {{ state.label }}
                                </option>
                            </select>
                        </div>

                        <div class="space-y-2">
                            <label class="text-xs uppercase font-bold text-slate-400">Image File</label>
                            <input type="file" @change="handleFileSelect" accept="image/*" class="block w-full text-sm text-slate-400
                                file:mr-4 file:py-2 file:px-4
                                file:rounded-full file:border-0
                                file:text-sm file:font-semibold
                                file:bg-indigo-500 file:text-white
                                hover:file:bg-indigo-600
                            "/>
                        </div>
                    </div>

                    <div class="flex justify-end pt-2">
                        <button 
                            @click="handleUpload" 
                            :disabled="!selectedFile || isUploading"
                            class="px-6 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-bold flex items-center gap-2 disabled:opacity-50 transition-colors"
                        >
                            <Loader2 v-if="isUploading" class="w-4 h-4 animate-spin" />
                            <span v-else>Upload</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Existing Images List -->
            <div class="space-y-4">
                <h3 class="font-bold text-slate-400 text-sm uppercase">Existing Configurations</h3>
                
                <div v-if="isLoading" class="flex justify-center py-4">
                     <Loader2 class="w-6 h-6 animate-spin text-slate-500" />
                </div>

                <div v-else-if="images?.length === 0" class="text-center text-muted-foreground text-sm py-4">
                    No custom images configurations found.
                </div>

                <div v-else class="grid grid-cols-2 gap-4">
                    <div v-for="img in images" :key="img.id" class="bg-black/20 rounded-xl p-3 border border-white/5 flex gap-3 relative group">
                        <img :src="img.image" class="w-16 h-16 object-contain rounded bg-black/20" />
                        <div class="flex-1 min-w-0 flex flex-col justify-center">
                            <div class="text-xs font-bold text-slate-400 uppercase">STATE</div>
                            <div class="text-sm font-bold text-white break-words">{{ getStateLabel(img.state) }}</div>
                        </div>
                        
                        <!-- Delete Button -->
                        <button 
                            @click="handleDelete(img.id)"
                            :disabled="deletingId === img.id"
                            class="absolute top-2 right-2 p-1.5 bg-red-500/20 text-red-400 rounded-md opacity-0 group-hover:opacity-100 transition-all hover:bg-red-500 hover:text-white"
                            title="Delete"
                        >
                            <Loader2 v-if="deletingId === img.id" class="w-4 h-4 animate-spin" />
                            <Trash2 v-else class="w-4 h-4" />
                        </button>
                    </div>
                </div>
            </div>

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
