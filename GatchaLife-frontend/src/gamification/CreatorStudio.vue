<script setup lang="ts">
import { ref } from 'vue';
import CharacterListView from '@/character/views/CharacterListView.vue';
import StyleListView from '@/style/views/StyleListView.vue';
import ThemeListView from '@/style/views/ThemeListView.vue';
import SeriesListView from '@/series/views/SeriesListView.vue';
import { Users, Palette, Image, Book } from 'lucide-vue-next';

const activeTab = ref('characters');

const tabs = [
  { id: 'characters', label: 'Characters', icon: Users, component: CharacterListView },
  { id: 'series', label: 'Series', icon: Book, component: SeriesListView },
  { id: 'styles', label: 'Styles', icon: Palette, component: StyleListView },
  { id: 'themes', label: 'Themes', icon: Image, component: ThemeListView },
];
</script>

<template>
  <div class="min-h-screen bg-background text-foreground pb-20 font-sans">
    <!-- Header -->
    <div class="sticky top-0 z-40 border-b border-border/50 bg-background/80 backdrop-blur-xl">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div class="flex items-center gap-2 cursor-pointer" @click="$router.push('/')">
          <div class="h-8 w-8 rounded-lg bg-gradient-to-br from-primary to-purple-600 flex items-center justify-center text-white font-bold">
            G
          </div>
          <span class="font-bold text-lg tracking-tight">Creator Studio</span>
        </div>
        <button @click="$router.push('/')" class="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
          Back to Dashboard
        </button>
      </div>
    </div>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="flex flex-col md:flex-row gap-8">
        <!-- Sidebar Navigation -->
        <aside class="w-full md:w-64 space-y-2">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all"
            :class="[
              activeTab === tab.id 
                ? 'bg-primary text-primary-foreground shadow-lg shadow-primary/20' 
                : 'hover:bg-muted text-muted-foreground hover:text-foreground'
            ]"
          >
            <component :is="tab.icon" class="w-5 h-5" />
            {{ tab.label }}
          </button>
        </aside>

        <!-- Content Area -->
        <div class="flex-1 bg-card border border-border rounded-3xl shadow-sm min-h-[500px] overflow-hidden">
          <component :is="tabs.find(t => t.id === activeTab)?.component" />
        </div>
      </div>
    </main>
  </div>
</template>
