<template>
  <div class="max-w-2xl mx-auto p-6">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl font-bold">All Series</h1>
      <router-link to="/character/new">
        <Button variant="outline">
          <Plus class="w-4 h-4 mr-2" /> New Character
        </Button>
      </router-link>
    </div>

    <div v-if="isLoading" class="text-center text-muted-foreground">Loading series...</div>

    <div v-else-if="series?.length === 0" class="text-center py-12 border-2 border-dashed rounded-lg">
      <p class="text-muted-foreground mb-2">No series found.</p>
      <router-link to="/character/new">
        <Button variant="link">Start by creating a character and a new series</Button>
      </router-link>
    </div>

    <div v-else class="space-y-4">
      <Card v-for="s in series" :key="s.id">
        <CardHeader class="flex flex-row items-center justify-between">
          <div>
            <CardTitle>{{ s.name }}</CardTitle>
            <CardDescription>{{ s.description || 'No description' }}</CardDescription>
          </div>
          <div class="flex gap-2">
            <Button variant="ghost" size="icon" @click="openEditDialog(s)">
              <Pencil class="w-4 h-4" />
            </Button>
            <AlertDialog>
              <AlertDialogTrigger as-child>
                <Button variant="ghost" size="icon" class="text-destructive hover:text-destructive">
                  <Trash2 class="w-4 h-4" />
                </Button>
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                  <AlertDialogDescription>
                    This will permanently delete the series "{{ s.name }}". This action cannot be undone.
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>Cancel</AlertDialogCancel>
                  <AlertDialogAction @click="handleDelete(s.id!)">Delete</AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          </div>
        </CardHeader>
      </Card>
    </div>

    <!-- Edit Dialog -->
    <Dialog v-model:open="isEditDialogOpen">
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Edit Series</DialogTitle>
        </DialogHeader>
        <div class="grid gap-4 py-4" v-if="editableSeries">
          <div class="space-y-2">
            <Label>Name</Label>
            <Input v-model="editableSeries.name" />
          </div>
          <div class="space-y-2">
            <Label>Description</Label>
            <Textarea v-model="editableSeries.description" />
          </div>
        </div>
        <DialogFooter>
          <Button @click="handleUpdate" :disabled="isUpdating">
            {{ isUpdating ? 'Saving...' : 'Save Changes' }}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Plus, Pencil, Trash2 } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from '@/components/ui/alert-dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { useSeriesList, useUpdateSeries, useDeleteSeries } from '@/lib/api-client'
import type { Series } from '@/api'

const { data: series, isLoading } = useSeriesList()
const { mutate: updateSeries, isPending: isUpdating } = useUpdateSeries()
const { mutate: deleteSeries } = useDeleteSeries()

const isEditDialogOpen = ref(false)
const editableSeries = ref<Partial<Series> | null>(null)

const openEditDialog = (series: Series) => {
  editableSeries.value = { ...series }
  isEditDialogOpen.value = true
}

const handleUpdate = () => {
  if (editableSeries.value?.id && editableSeries.value.name) {
    updateSeries(editableSeries.value as Series, {
      onSuccess: () => {
        isEditDialogOpen.value = false
      }
    })
  }
}

const handleDelete = (id: number) => {
  deleteSeries(id)
}
</script>
