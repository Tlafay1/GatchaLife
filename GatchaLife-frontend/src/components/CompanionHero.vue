<template>
  <div class="companion-hero" v-if="state" @click="interact">
    <!-- Character Image Container -->
    <div class="character-container" :class="{ 'breathing': !isBouncing, 'bouncing': isBouncing }">
      <img 
        :src="state.image_url || defaultImage" 
        :alt="state.character_name"
        class="character-image"
        @error="handleImageError"
      />
    </div>

    <!-- Dialogue Bubble -->
    <div class="dialogue-bubble" v-if="displayedText">
      <p class="dialogue-text">{{ displayedText }}</p>
    </div>
  </div>
  
  <!-- Loading / Empty State -->
  <div class="companion-hero empty" v-else-if="loading">
    <div class="skeleton-character"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue';

interface CompanionState {
  status: string;
  character_name: string;
  mood_state: string;
  image_url: string | null;
  dialogue_text: string;
  productivity_score: number;
}

const props = defineProps<{
  state: CompanionState | null;
  loading?: boolean;
}>();

const isBouncing = ref(false);
const displayedText = ref('');
const defaultImage = '/images/placeholder_companion.svg'; // Updated to SVG

// Typewriter Effect
const typeSpeed = 30; // ms per char

const startTypewriter = (text: string) => {
  displayedText.value = '';
  if (!text) return;
  
  let i = 0;
  const typeKey = setInterval(() => {
    displayedText.value += text.charAt(i);
    i++;
    if (i >= text.length) {
      clearInterval(typeKey);
    }
  }, typeSpeed);
};

watch(() => props.state?.dialogue_text, (newText) => {
  if (newText) {
    startTypewriter(newText);
  }
}, { immediate: true });

const interact = () => {
  if (isBouncing.value) return;
  
  // Bounce Animation
  isBouncing.value = true;
  // Play sound effect here if desired
  
  setTimeout(() => {
    isBouncing.value = false;
  }, 500); // Duration of bounce
};

const handleImageError = (e: Event) => {
  const img = e.target as HTMLImageElement;
  // Prevent infinite loop if default image also fails
  if (img.src.includes(defaultImage)) {
    return;
  }
  img.src = defaultImage;
};

// CSS Variables for Mood Styling if needed
const moodColor = computed(() => {
  switch (props.state?.mood_state) {
    case 'SAD': return '#bdc3c7';
    case 'HAPPY': return '#f1c40f';
    case 'EXCITED': return '#e74c3c';
    default: return '#95a5a6';
  }
});

</script>

<style scoped>
.companion-hero {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  min-height: 400px;
  cursor: pointer;
  user-select: none;
}

.character-container {
  position: relative;
  z-index: 2;
  transition: transform 0.3s ease;
}

.character-image {
  max-height: 350px;
  width: auto;
  filter: drop-shadow(0 10px 20px rgba(0,0,0,0.3));
}

/* Breathing Animation */
@keyframes breathe {
  0% { transform: scale(1); }
  50% { transform: scale(1.03); }
  100% { transform: scale(1); }
}

.breathing {
  animation: breathe 4s ease-in-out infinite;
}

/* Bounce Animation */
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

.bouncing {
  animation: bounce 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.dialogue-bubble {
  margin-top: 1.5rem;
  background: rgba(255, 255, 255, 0.95);
  padding: 1rem 1.5rem;
  border-radius: 20px;
  border-bottom-left-radius: 0;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  max-width: 80%;
  position: relative;
  z-index: 3;
  backdrop-filter: blur(5px);
  /* Speech bubble tail */
}

.dialogue-bubble::before {
  content: '';
  position: absolute;
  top: -10px;
  left: 30px;
  border-width: 0 10px 10px;
  border-style: solid;
  border-color: transparent transparent rgba(255, 255, 255, 0.95);
}

.dialogue-text {
  color: #2c3e50;
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 1.1rem;
  line-height: 1.5;
  margin: 0;
}

.skeleton-character {
  width: 200px;
  height: 300px;
  background: rgba(255,255,255,0.1);
  border-radius: 20px;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 0.8; }
  100% { opacity: 0.6; }
}
</style>
