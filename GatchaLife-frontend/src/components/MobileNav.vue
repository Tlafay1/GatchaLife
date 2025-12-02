<script setup lang="ts">
import { Home, Grid, Sparkles, History, PenTool } from 'lucide-vue-next';
import { useRoute } from 'vue-router';

const route = useRoute();

const isActive = (path: string) => route.path === path;

const navItems = [
  { name: 'Home', path: '/', icon: Home },
  { name: 'Collection', path: '/collection', icon: Grid },
  { name: 'Summon', path: '/gatcha', icon: Sparkles, special: true },
  { name: 'History', path: '/history', icon: History },
  { name: 'Creator', path: '/creator', icon: PenTool },
];
</script>

<template>
  <nav class="fixed bottom-0 left-0 right-0 z-50 bg-background/95 backdrop-blur border-t border-border pb-safe">
    <div class="flex items-center justify-around h-16 px-2">
      <router-link 
        v-for="item in navItems" 
        :key="item.path" 
        :to="item.path"
        class="flex flex-col items-center justify-center w-full h-full space-y-1 transition-colors relative"
        :class="[
          isActive(item.path) ? 'text-primary' : 'text-muted-foreground hover:text-foreground',
          item.special ? '-mt-6' : ''
        ]"
      >
        <div v-if="item.special" class="bg-primary text-primary-foreground p-3 rounded-full shadow-lg border-4 border-background">
          <component :is="item.icon" class="w-6 h-6" />
        </div>
        <component v-else :is="item.icon" class="w-5 h-5" />
        
        <span v-if="!item.special" class="text-[10px] font-medium">{{ item.name }}</span>
      </router-link>
    </div>
  </nav>
</template>

<style scoped>
.pb-safe {
  padding-bottom: env(safe-area-inset-bottom);
}
</style>
