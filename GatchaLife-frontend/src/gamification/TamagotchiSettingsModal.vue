<script setup lang="ts">
import { ref, watch } from 'vue';
import { useUpdateTamagotchi } from '@/lib/api-client';
import { Settings, Moon, Sun, Save, X } from 'lucide-vue-next';

const props = defineProps<{
  show: boolean;
  tamagotchi: {
    id: number;
    name: string;
    sleep_start_hour: number;
    sleep_end_hour: number;
  } | null;
}>();

const emit = defineEmits(['close']);

const form = ref({
  name: '',
  sleep_start_hour: 23,
  sleep_end_hour: 7,
});

const { mutate: update, isPending } = useUpdateTamagotchi();

watch(() => props.show, (newVal) => {
  if (newVal && props.tamagotchi) {
    form.value = {
      name: props.tamagotchi.name,
      sleep_start_hour: props.tamagotchi.sleep_start_hour,
      sleep_end_hour: props.tamagotchi.sleep_end_hour,
    };
  }
});

const handleUpdate = () => {
  if (!props.tamagotchi) return;
  update({
    id: props.tamagotchi.id,
    ...form.value
  }, {
    onSuccess: () => {
      emit('close');
    }
  });
};

const hours: number[] = [];
for (let i = 0; i < 24; i++) {
  hours.push(i);
}
const formatHour = (h: number) => {
  const ampm = h >= 12 ? 'PM' : 'AM';
  const hour12 = h % 12 || 12;
  return `${hour12}:00 ${ampm}`;
};
</script>

<template>
  <Teleport to="body">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm px-4">
      <div 
        class="bg-card border border-border rounded-xl shadow-2xl max-w-md w-full p-6 animate-in fade-in zoom-in-95 duration-200"
      >
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-xl font-bold flex items-center gap-2">
            <Settings class="w-5 h-5 text-muted-foreground" />
            Companion Settings
          </h3>
          <button @click="$emit('close')" class="text-muted-foreground hover:text-foreground transition-colors">
            <X class="w-5 h-5" />
          </button>
        </div>

        <form @submit.prevent="handleUpdate" class="space-y-6">
          <!-- Name Input -->
          <div class="space-y-2">
            <label class="text-sm font-bold text-muted-foreground">Name</label>
            <input 
              v-model="form.name" 
              type="text" 
              class="w-full px-3 py-2 bg-secondary/50 border border-transparent rounded-lg focus:ring-2 focus:ring-primary/50 focus:outline-none transition-all font-bold"
            />
          </div>

          <!-- Sleep Schedule -->
          <div class="space-y-4">
            <label class="text-sm font-bold text-muted-foreground flex items-center gap-2">
              <Moon class="w-4 h-4" /> Sleep Schedule
            </label>
            <div class="p-4 bg-secondary/30 rounded-lg border border-border/50 space-y-4">
              <p class="text-xs text-muted-foreground">
                Your companion will sleep during these hours. Decay is paused while sleeping.
              </p>
              
              <div class="grid grid-cols-2 gap-4">
                <div class="space-y-2">
                  <label class="text-xs font-bold text-muted-foreground">Sleep at</label>
                  <select v-model="form.sleep_start_hour" class="w-full px-2 py-2 bg-background border border-input rounded-md text-sm">
                    <option v-for="h in hours" :key="h" :value="h">{{ formatHour(h) }}</option>
                  </select>
                </div>
                
                <div class="space-y-2">
                  <label class="text-xs font-bold text-muted-foreground">Wake up at</label>
                   <select v-model="form.sleep_end_hour" class="w-full px-2 py-2 bg-background border border-input rounded-md text-sm">
                    <option v-for="h in hours" :key="h" :value="h">{{ formatHour(h) }}</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          <button 
            type="submit" 
            :disabled="!form.name || isPending"
            class="w-full py-2.5 bg-primary hover:bg-primary/90 text-primary-foreground font-bold rounded-lg flex items-center justify-center gap-2 transition-all disabled:opacity-50"
          >
            <span v-if="isPending" class="animate-spin text-lg">⟳</span>
            <span v-else class="flex items-center gap-2">
              <Save class="w-4 h-4" /> Save Changes
            </span>
          </button>
        </form>
      </div>
    </div>
  </Teleport>
</template>
