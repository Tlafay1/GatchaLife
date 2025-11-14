<template>
  <div class="max-w-4xl mx-auto p-6">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl font-bold">Character Dashboard</h1>
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

    <div v-if="isLoading" class="text-center text-muted-foreground">Loading characters...</div>

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
          <Card v-for="char in group.characters" :key="char.id">
            <CardHeader>
              <CardTitle>{{ char.name }}</CardTitle>
            </CardHeader>
            <CardContent>
              <p class="text-sm text-muted-foreground truncate">{{ char.description || 'No description' }}</p>
            </CardContent>
            <CardFooter>
              <router-link :to="`/character/${char.id}/edit`" class="w-full">
                <Button variant="outline" class="w-full">Edit</Button>
              </router-link>
            </CardFooter>
          </Card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Plus } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card'
import { useCharactersList } from '@/lib/api-client'
import type { Character, Series } from '@/api'

const { data: characters, isLoading } = useCharactersList()

interface SeriesGroup {
  series: Series;
  characters: Character[];
}

const charactersBySeries = computed<SeriesGroup[]>(() => {
  if (!characters.value) return []

  const groups: Record<number, SeriesGroup> = {}

  characters.value.forEach(char => {
    if (!char.series) return;
    const seriesId = (char.series as Series).id!
    if (!groups[seriesId]) {
      groups[seriesId] = {
        series: char.series as Series,
        characters: []
      }
    }
    groups[seriesId].characters.push(char)
  })

  return Object.values(groups)
})
</script>
