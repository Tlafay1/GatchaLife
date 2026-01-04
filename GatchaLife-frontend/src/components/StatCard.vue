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
   class="relative overflow-hidden rounded-2xl border border-white/5 p-6 shadow-lg backdrop-blur-md transition-all duration-300 group"
    :class="[clickable ? 'hover:scale-[1.02] hover:shadow-xl cursor-pointer' : '', $attrs.class ? '' : 'bg-black/20']"
  >
    <!-- Background Gradient -->
    <div v-if="bgGradient"
      :class="['absolute inset-0 bg-gradient-to-br opacity-40 transition-opacity group-hover:opacity-60', bgGradient]">
    </div>
    
    <div class="relative z-10 flex items-center justify-between">
      <div>
        <div
          class="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-1 group-hover:text-slate-200 transition-colors">
          {{ title }}</div>
        <div :class="['text-3xl font-black tracking-tighter drop-shadow-sm', color || 'text-white']">
          {{ value }}
        </div>
      </div>
      
<div v-if="icon"
        :class="['p-3 rounded-xl bg-white/5 backdrop-blur-md shadow-inner border border-white/10', color]">
        <component :is="icon" class="w-6 h-6 group-hover:scale-110 transition-transform" />
      </div>
    </div>
  </div>
</template>
