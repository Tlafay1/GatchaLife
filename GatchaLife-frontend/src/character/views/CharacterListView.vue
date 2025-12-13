<template>
  <div class="max-w-4xl mx-auto p-6">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl font-bold">Character Dashboard</h1>
      <div class="flex items-center gap-4">
        <div class="flex items-center space-x-2 border px-3 py-2 rounded-md bg-background">
           <input type="checkbox" id="show-archived-chars" v-model="showArchived" class="h-4 w-4 rounded border-input" />
           <label for="show-archived-chars" class="cursor-pointer text-sm">Show Archived</label>
        </div>
        <div class="flex gap-2">
          <router-link to="/series">
            <Button variant="outline">All Series</Button>
          </router-link>
          <router-link to="/character/new">
            <Button>
              <Plus class="w-4 h-4 mr-2" /> New Character
            </Button>
          </router-link>
        </div>
      </div>
    </div>

    <div v-if="isCharactersLoading" class="text-center text-muted-foreground">Loading characters...</div>

    <div v-else-if="charactersBySeries.length === 0" class="text-center py-12 border-2 border-dashed rounded-lg">
      <p class="text-muted-foreground mb-2">No characters found.</p>
      <router-link to="/character/new">
        <Button variant="link">Create your first character</Button>
      </router-link>
    </div>

    <div v-else class="space-y-6">
      <div v-for="group in charactersBySeries" :key="group.series.id">
        <h2 class="text-xl font-semibold mb-3">{{ group.series.name }}</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <Card v-for="char in group.characters" :key="char.id" 
                :class="char.legacy ? 'opacity-70 grayscale bg-muted/20 border-dashed' : ''">
            <CardHeader class="pb-2">
              <div class="flex justify-between items-start">
                  <CardTitle>{{ char.name }}</CardTitle>
                  <span v-if="char.legacy" class="px-1.5 py-0.5 rounded text-[10px] uppercase font-bold border bg-neutral-800/80 text-white border-white/10 shrink-0 ml-2">Legacy</span>
              </div>
            </CardHeader>
            <CardContent>
              <p class="text-sm text-muted-foreground truncate">{{ char.description || 'No description' }}</p>
            </CardContent>
            <CardFooter class="flex gap-2">
              <router-link :to="`/character/${char.id}/edit`" class="w-full">
                <Button variant="outline" class="w-full">Edit</Button>
              </router-link>
              <Button variant="ghost" size="icon" class="text-destructive hover:text-destructive" @click="handleDelete(char.id!)">
                <Trash2 class="w-4 h-4" />
              </Button>
            </CardFooter>
          </Card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { Plus, Trash2 } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card'
import { useCharactersList, useSeriesList, useDeleteCharacter } from '@/lib/api-client'
import type { Character, Series } from '@/api'

const showArchived = ref(false)
const { data: characters, isLoading: isCharactersLoading } = useCharactersList()
const { data: series } = useSeriesList()

const { mutate: deleteCharacter } = useDeleteCharacter()

const handleDelete = (id: number) => {
  if (confirm('Are you sure you want to delete this character?')) {
    deleteCharacter(id)
  }
}

interface SeriesGroup {
  series: Series;
  characters: Character[];
}

const charactersBySeries = computed<SeriesGroup[]>(() => {
  if (!characters.value) return []

  const groups: Record<number, SeriesGroup> = {}

  characters.value.forEach(char => {
    // Filter for archived
    if (!showArchived.value && char.legacy) return;

    if (!char.series) return;
    const seriesId = char.series
    if (!groups[seriesId]) {
      const foundSeries = series.value?.find(s => s.id === seriesId);
      if (foundSeries) {
        groups[seriesId] = {
          series: foundSeries,
          characters: []
        }
      } else {
        // Fallback or skip if series not found (shouldn't happen with proper FKs)
        return;
      }
    }
    groups[seriesId].characters.push(char)
  })

  return Object.values(groups)
})
</script>
