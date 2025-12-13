<script setup lang="ts">
import {
  useCollection,
  useThemesList,
  useStylesList,
  useSeriesList,
  useRaritiesList
} from '@/lib/api-client';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { Search, FilterX, SlidersHorizontal, ChevronDown, ChevronUp, Maximize2, X } from 'lucide-vue-next';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

const router = useRouter();
const filters = ref({
  rarity: 'all',
  theme: 'all',
  style: 'all',
  series: 'all',
  series: 'all',
  character: '', // Search by name
  showArchived: false,
});

const groupBy = ref('series'); // Default group by
const isFiltersOpen = ref(false); // Minimized by default
const selectedCard = ref<any>(null); // For full screen view

// Transform "all" to empty string for API
const apiFilters = computed(() => {
  const f = { ...filters.value };
  if (f.rarity === 'all') f.rarity = '';
  if (f.theme === 'all') f.theme = '';
  if (f.style === 'all') f.style = '';
  if (f.series === 'all') f.series = '';
  return f;
});

const { data: collection, isLoading } = useCollection(apiFilters);
const { data: themes } = useThemesList();
const { data: styles } = useStylesList();
const { data: series } = useSeriesList();
const { data: rarities } = useRaritiesList();

const resetFilters = () => {
  filters.value = {
    rarity: 'all',
    theme: 'all',
    style: 'all',
    series: 'all',
    series: 'all',
    character: '',
    showArchived: false,
  };
  groupBy.value = 'series';
};

const groupedCollection = computed(() => {
  if (!collection.value) return {};

  if (groupBy.value === 'none') {
    return { 'All Cards': collection.value };
  }

  const groups: Record<string, any[]> = {};

  collection.value.forEach((item: any) => {
    // Filter Archived
    if (!filters.value.showArchived && item.card.is_archived) {
      return;
    }

    let key = 'Other';
    const card = item.card;

    switch (groupBy.value) {
      case 'series': key = card.series_name || 'Unknown Series'; break;
      case 'rarity': key = card.rarity_name || 'Unknown Rarity'; break;
      case 'theme': key = card.theme_name || 'Unknown Theme'; break;
      case 'style': key = card.style_name || 'Unknown Style'; break;
    }

    if (!groups[key]) groups[key] = [];
    const group = groups[key];
    if (group) {
      group.push(item);
    }
  });

  // Sort keys
  let keys = Object.keys(groups);

  if (groupBy.value === 'rarity' && rarities.value) {
    // Sort by rarity threshold descending (Legendary -> Common)
    keys.sort((a, b) => {
      const rA = rarities.value?.find((r: any) => r.name === a);
      const rB = rarities.value?.find((r: any) => r.name === b);
      // If rarity not found (e.g. "Other"), push to end
      if (!rA) return 1;
      if (!rB) return -1;
      return rB.min_roll_threshold - rA.min_roll_threshold;
    });
  } else {
    keys.sort();
  }

  return keys.reduce(
    (obj, key) => {
      obj[key] = groups[key] || [];
      return obj;
    },
    {} as Record<string, any[]>
  );
});

const rarityColor = (rarity: string) => {
  switch (rarity?.toLowerCase()) {
    case 'common': return 'border-gray-500/50 shadow-gray-500/20';
    case 'rare': return 'border-blue-500/50 shadow-blue-500/20';
    case 'legendary': return 'border-yellow-500/50 shadow-yellow-500/20';
    default: return 'border-border';
  }
};

const goToDetails = (id: number) => {
  router.push(`/collection/${id}`);
};

const openFullScreen = (item: any) => {
  selectedCard.value = item;
};

const closeFullScreen = () => {
  selectedCard.value = null;
};
</script>

<template>
  <div class="min-h-screen bg-background text-foreground p-4 md:p-8 font-sans">
    <div class="max-w-7xl mx-auto space-y-8">
      <!-- Header -->
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 class="text-3xl font-bold">My Collection</h1>
          <p class="text-muted-foreground">Manage and view your collected cards</p>
        </div>
        <div class="flex items-center gap-4">
          <Button variant="outline" @click="isFiltersOpen = !isFiltersOpen">
            <SlidersHorizontal class="w-4 h-4 mr-2" />
            Filters & Sorting
            <component :is="isFiltersOpen ? ChevronUp : ChevronDown" class="w-4 h-4 ml-2" />
          </Button>
          <router-link to="/" class="hidden md:block text-muted-foreground hover:text-foreground transition-colors">
            ← Back to Dashboard
          </router-link>
        </div>
      </div>

      <!-- Advanced Filters (Collapsible) -->
      <div v-if="isFiltersOpen" class="bg-card border border-border rounded-xl p-4 space-y-4">
        <div class="flex flex-col md:flex-row gap-4">
          <!-- Search -->
          <div class="relative flex-1">
            <Search class="absolute left-3 top-3 w-4 h-4 text-muted-foreground" />
            <Input v-model="filters.character" placeholder="Search characters..." class="pl-9" />
          </div>

          <!-- Group By -->
          <div class="w-full md:w-48">
            <Select v-model="groupBy">
              <SelectTrigger>
                <SelectValue placeholder="Group By" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="none">No Grouping</SelectItem>
                <SelectItem value="series">Series</SelectItem>
                <SelectItem value="rarity">Rarity</SelectItem>
                <SelectItem value="theme">Theme</SelectItem>
                <SelectItem value="style">Style</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <!-- Reset -->
          <Button variant="ghost" @click="resetFilters" class="shrink-0 text-muted-foreground hover:text-destructive">
            <FilterX class="w-4 h-4 mr-2" />
            Reset
          </Button>
        </div>
        
        <div class="flex items-center space-x-2 px-2 pb-2">
           <input type="checkbox" id="show-archived" v-model="filters.showArchived" class="h-4 w-4 rounded border-input" />
           <Label for="show-archived" class="text-sm cursor-pointer">Show Archived Cards</Label>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 pt-2 border-t border-border/50">
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

      <!-- Grid with Groups -->
      <div v-if="isLoading" class="text-center py-12 text-muted-foreground">
        Loading collection...
      </div>

      <div v-else-if="!collection?.length"
        class="text-center py-12 text-muted-foreground bg-card rounded-xl border border-border">
        No cards found. Go summon some!
      </div>

      <div v-else class="space-y-8">
        <div v-for="(items, groupName) in groupedCollection" :key="groupName" class="space-y-4">
          <!-- Group Header -->
          <div v-if="groupBy !== 'none'" class="flex items-center gap-4">
            <h2 class="text-xl font-bold">{{ groupName }}</h2>
            <div class="h-px flex-1 bg-border"></div>
            <span class="text-sm text-muted-foreground">{{ items.length }} cards</span>
          </div>

          <!-- Cards Grid -->
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
            <div v-for="item in items" :key="item.id" @click="goToDetails(item.id)"
              class="group relative aspect-[2/3] bg-card rounded-xl border-2 overflow-hidden transition-all hover:scale-105 hover:z-10 cursor-pointer block"
              :class="[rarityColor(item.card.rarity_name), item.card.is_archived ? 'grayscale-[0.7] opacity-90' : '']">
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

              <!-- Count Badge (moved to left) -->
              <div v-if="item.count > 1"
                class="absolute top-2 left-2 bg-black/60 backdrop-blur text-white text-xs font-bold px-2 py-1 rounded-full border border-white/20 z-20">
                x{{ item.count }}
              </div>
              <div v-if="item.card.is_archived"
                class="absolute top-2 right-2 bg-neutral-800/80 backdrop-blur text-white text-[10px] uppercase font-bold px-2 py-0.5 rounded border border-white/10 z-20">
                Legacy
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Full Screen Modal -->
    <Teleport to="body">
      <div v-if="selectedCard" class="fixed inset-0 z-50 flex items-center justify-center bg-black/95 backdrop-blur-sm p-4"
        @click="closeFullScreen">
        
        <!-- Close Button -->
        <button @click="closeFullScreen" class="absolute top-4 right-4 p-2 text-white/70 hover:text-white bg-white/10 hover:bg-white/20 rounded-full transition-colors z-50">
          <X class="w-8 h-8" />
        </button>

        <!-- Image Container -->
        <div class="relative w-full h-full max-w-5xl max-h-[90vh] flex items-center justify-center" @click.stop>
          <img 
            v-if="selectedCard.card.image_url" 
            :src="selectedCard.card.image_url" 
            class="max-w-full max-h-full object-contain rounded-lg shadow-2xl"
          />
          
          <!-- Info Overlay (Bottom) -->
          <div class="absolute bottom-0 inset-x-0 p-6 bg-gradient-to-t from-black/90 to-transparent text-white text-center">
            <div class="text-sm font-bold uppercase tracking-wider opacity-80 mb-1">{{ selectedCard.card.rarity_name }}</div>
            <h2 class="text-2xl font-bold">{{ selectedCard.card.character_variant_name }}</h2>
            <p class="text-white/60 text-sm mt-1">{{ selectedCard.card.series_name }}</p>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
