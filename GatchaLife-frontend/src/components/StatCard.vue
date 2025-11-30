<script setup lang="ts">
import type { Component } from 'vue';

defineProps<{
  title: string;
  value: string | number;
  icon?: Component;
  color?: string; // e.g. 'text-blue-500'
  bgGradient?: string; // e.g. 'from-blue-500/20 to-blue-500/5'
  clickable?: boolean;
}>();
</script>

<template>
  <div 
    class="relative overflow-hidden rounded-2xl border border-border/50 bg-card/50 p-6 shadow-lg backdrop-blur-sm transition-all duration-300 group"
    :class="[clickable ? 'hover:scale-[1.02] hover:shadow-xl cursor-pointer' : '']"
  >
    <!-- Background Gradient -->
    <div v-if="bgGradient" :class="['absolute inset-0 bg-gradient-to-br opacity-50 transition-opacity group-hover:opacity-70', bgGradient]"></div>
    
    <div class="relative z-10 flex items-center justify-between">
      <div>
        <div class="text-sm font-bold uppercase tracking-wider text-muted-foreground/80 mb-1">{{ title }}</div>
        <div :class="['text-3xl font-black tracking-tight', color || 'text-foreground']">
          {{ value }}
        </div>
      </div>
      
      <div v-if="icon" :class="['p-3 rounded-xl bg-background/50 backdrop-blur-md shadow-sm', color]">
        <component :is="icon" class="w-8 h-8" />
      </div>
    </div>
  </div>
</template>
