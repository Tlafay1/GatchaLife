<template>
  <div class="max-w-2xl mx-auto p-6">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl font-bold">All Series</h1>
      <Button @click="openCreateDialog">
        <Plus class="w-4 h-4 mr-2" /> New Series
      </Button>
    </div>

    <div v-if="isLoading" class="text-center text-muted-foreground">Loading series...</div>

    <div v-else-if="series?.length === 0" class="text-center py-12 border-2 border-dashed rounded-lg">
      <p class="text-muted-foreground mb-2">No series found.</p>
      <Button variant="link" @click="openCreateDialog">Create your first series</Button>
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
            <Button variant="ghost" size="icon" class="text-destructive hover:text-destructive"
              @click="handleDelete(s.id!)">
              <Trash2 class="w-4 h-4" />
            </Button>
          </div>
        </CardHeader>
      </Card>
    </div>

    <!-- Create/Edit Dialog -->
    <Dialog v-model:open="isDialogOpen">
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{{ isEditing ? 'Edit Series' : 'Create New Series' }}</DialogTitle>
        </DialogHeader>
        <div class="grid gap-4 py-4">
          <div class="space-y-2">
            <Label>Name</Label>
            <Input v-model="form.name" placeholder="e.g. Mushoku Tensei" />
          </div>
          <div class="space-y-2">
            <Label>Unlock Level</Label>
            <Input v-model="form.unlock_level" type="number" min="1" placeholder="1" />
            <p class="text-xs text-muted-foreground">Player level required to unlock this series.</p>
          </div>
          <div class="space-y-2">
            <Label>Description</Label>
            <Textarea v-model="form.description" placeholder="Series description..." />
          </div>
        </div>
        <DialogFooter>
          <Button @click="handleSubmit" :disabled="isSubmitting">
            {{ isSubmitting ? 'Saving...' : 'Save Series' }}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { Plus, Pencil, Trash2 } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { useSeriesList, useCreateSeries, useUpdateSeries, useDeleteSeries } from '@/lib/api-client'
import type { Series } from '@/api'

const { data: series, isLoading } = useSeriesList()
const { mutateAsync: createSeries, isPending: isCreating } = useCreateSeries()
const { mutateAsync: updateSeries, isPending: isUpdating } = useUpdateSeries()
const { mutate: deleteSeries } = useDeleteSeries()

const isDialogOpen = ref(false)
const editingId = ref<number | null>(null)
const isEditing = computed(() => !!editingId.value)
const isSubmitting = computed(() => isCreating.value || isUpdating.value)

const form = reactive({
  name: '',
  description: '',
  unlock_level: 1
})

const openCreateDialog = () => {
  editingId.value = null
  form.name = ''
  form.description = ''
  form.unlock_level = 1
  isDialogOpen.value = true
}

const openEditDialog = (series: Series) => {
  editingId.value = series.id!
  form.name = series.name
  form.description = series.description || ''
  form.unlock_level = series.unlock_level || 1
  isDialogOpen.value = true
}

const handleSubmit = async () => {
  if (!form.name) {
    alert('Name is required')
    return
  }

  try {
    const payload = {
      name: form.name,
      description: form.description,
      unlock_level: form.unlock_level
    }

    if (isEditing.value && editingId.value) {
      await updateSeries({ id: editingId.value, ...payload })
    } else {
      await createSeries(payload)
    }
    isDialogOpen.value = false
  } catch (error) {
    console.error(error)
    alert('Failed to save series')
  }
}

const handleDelete = (id: number) => {
  if (confirm('Are you sure you want to delete this series?')) {
    deleteSeries(id)
  }
}
</script>
