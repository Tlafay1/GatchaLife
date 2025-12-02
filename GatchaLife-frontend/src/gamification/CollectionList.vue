<script setup lang="ts">
import {
  useCollection,
  useThemesList,
  useStylesList,
  useSeriesList,
  useRaritiesList
} from '@/lib/api-client';
import { ref } from 'vue';
import { Search, FilterX } from 'lucide-vue-next';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

const filters = ref({
  rarity: '',
  theme: '',
  style: '',
  series: '',
  character: '', // Search by name
});

const { data: collection, isLoading } = useCollection(filters);
const { data: themes } = useThemesList();
const { data: styles } = useStylesList();
const { data: series } = useSeriesList();
const { data: rarities } = useRaritiesList();

const resetFilters = () => {
  filters.value = {
    rarity: '',
    theme: '',
    style: '',
    series: '',
    character: '',
  };
};

const rarityColor = (rarity: string) => {
  switch (rarity?.toLowerCase()) {
    case 'common': return 'border-gray-500/50 shadow-gray-500/20';
    case 'rare': return 'border-blue-500/50 shadow-blue-500/20';
    case 'legendary': return 'border-yellow-500/50 shadow-yellow-500/20';
    default: return 'border-border';
  }
};
</script>

<template>
  <div class="min-h-screen bg-background text-foreground p-8 font-sans">
    <div class="max-w-7xl mx-auto space-y-8">
      <!-- Header -->
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 class="text-3xl font-bold">My Collection</h1>
          <p class="text-muted-foreground">Manage and view your collected cards</p>
        </div>
        <router-link to="/" class="text-muted-foreground hover:text-foreground transition-colors">
          ← Back to Dashboard
        </router-link>
      </div>

      <!-- Advanced Filters -->
      <div class="bg-card border border-border rounded-xl p-4 space-y-4">
        <div class="flex flex-col md:flex-row gap-4">
          <!-- Search -->
          <div class="relative flex-1">
            <Search class="absolute left-3 top-3 w-4 h-4 text-muted-foreground" />
            <Input v-model="filters.character" placeholder="Search characters..." class="pl-9" />
          </div>

          <!-- Reset -->
          <Button variant="outline" @click="resetFilters" class="shrink-0">
            <FilterX class="w-4 h-4 mr-2" />
            Reset Filters
          </Button>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <!-- Rarity -->
          <Select v-model="filters.rarity">
            <SelectTrigger>
              <SelectValue placeholder="Rarity" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Rarities</SelectItem>
              <SelectItem v-for="r in rarities" :key="r.id" :value="r.name">
                {{ r.name }}
              </SelectItem>
            </SelectContent>
          </Select>

          <!-- Theme -->
          <Select v-model="filters.theme">
            <SelectTrigger>
              <SelectValue placeholder="Theme" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Themes</SelectItem>
              <SelectItem v-for="t in themes" :key="t.id" :value="t.name">
                {{ t.name }}
              </SelectItem>
            </SelectContent>
          </Select>

          <!-- Style -->
          <Select v-model="filters.style">
            <SelectTrigger>
              <SelectValue placeholder="Style" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Styles</SelectItem>
              <SelectItem v-for="s in styles" :key="s.id" :value="s.name">
                {{ s.name }}
              </SelectItem>
            </SelectContent>
          </Select>

          <!-- Series -->
          <Select v-model="filters.series">
            <SelectTrigger>
              <SelectValue placeholder="Series" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Series</SelectItem>
              <SelectItem v-for="s in series" :key="s.id" :value="s.name">
                {{ s.name }}
              </SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <!-- Grid -->
      <div v-if="isLoading" class="text-center py-12 text-muted-foreground">
        Loading collection...
      </div>

      <div v-else-if="!collection?.length"
        class="text-center py-12 text-muted-foreground bg-card rounded-xl border border-border">
        No cards found. Go summon some!
      </div>

      <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
        <router-link v-for="item in collection" :key="item.id" :to="`/collection/${item.id}`"
          class="group relative aspect-[2/3] bg-card rounded-xl border-2 overflow-hidden transition-all hover:scale-105 hover:z-10 cursor-pointer block"
          :class="rarityColor(item.card.rarity_name)">
          <!-- Image -->
          <div class="absolute inset-0 bg-muted">
            <img v-if="item.card.image_url" :src="item.card.image_url"
              class="w-full h-full object-cover transition-transform group-hover:scale-110" loading="lazy" />
            <div v-else class="w-full h-full flex items-center justify-center text-muted-foreground text-xs">
              Generating...
            </div>
          </div>

          <!-- Overlay Info -->
          <div
            class="absolute inset-x-0 bottom-0 p-3 bg-gradient-to-t from-black/90 via-black/60 to-transparent pt-12 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-end">
            <div class="text-xs font-bold text-white/80 uppercase">{{ item.card.rarity_name }}</div>
            <div class="font-bold text-white text-sm leading-tight">{{ item.card.character_variant_name }}</div>
            <div class="text-xs text-white/60 mt-1">x{{ item.count }}</div>
          </div>

          <!-- Count Badge (always visible) -->
          <div v-if="item.count > 1"
            class="absolute top-2 right-2 bg-black/60 backdrop-blur text-white text-xs font-bold px-2 py-1 rounded-full border border-white/20">
            x{{ item.count }}
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>
