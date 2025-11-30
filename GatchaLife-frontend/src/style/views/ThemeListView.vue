<template>
  <div class="max-w-4xl mx-auto p-6">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl font-bold">Themes</h1>
      <Button @click="openCreateDialog">
        <Plus class="w-4 h-4 mr-2" /> New Theme
      </Button>
    </div>

    <div v-if="isLoading" class="text-center text-muted-foreground">Loading themes...</div>

    <div v-else-if="themes?.length === 0" class="text-center py-12 border-2 border-dashed rounded-lg">
      <p class="text-muted-foreground mb-2">No themes found.</p>
      <Button variant="link" @click="openCreateDialog">Create your first theme</Button>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <Card v-for="theme in themes" :key="theme.id">
        <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
          <div>
            <CardTitle class="text-lg font-bold">{{ theme.name }}</CardTitle>
            <div class="text-xs text-muted-foreground mt-1">
              {{ theme.category }} • {{ theme.ambiance }}
            </div>
          </div>
          <div class="flex gap-2">
            <Button variant="ghost" size="icon" @click="openEditDialog(theme)">
              <Pencil class="w-4 h-4" />
            </Button>
            <Button variant="ghost" size="icon" class="text-destructive hover:text-destructive" @click="handleDelete(theme.id!)">
              <Trash2 class="w-4 h-4" />
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div class="space-y-2 text-sm">
            <div>
              <span class="text-muted-foreground block mb-1">Keywords:</span>
              <div class="bg-muted p-2 rounded text-xs font-mono break-all">{{ theme.keywords_theme }}</div>
            </div>
            <div v-if="theme.prompt_background">
              <span class="text-muted-foreground block mb-1">Background Prompt:</span>
              <div class="bg-muted p-2 rounded text-xs font-mono break-all">{{ theme.prompt_background }}</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Create/Edit Dialog -->
    <Dialog v-model:open="isDialogOpen">
      <DialogContent class="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>{{ isEditing ? 'Edit Theme' : 'Create New Theme' }}</DialogTitle>
          <DialogDescription>
            Define the theme setting and background prompts.
          </DialogDescription>
        </DialogHeader>
        
        <div class="grid gap-4 py-4 max-h-[60vh] overflow-y-auto px-1">
          <div class="grid gap-2">
            <Label>Name</Label>
            <Input v-model="form.name" placeholder="e.g. Cyberpunk City" />
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div class="grid gap-2">
              <Label>Category</Label>
              <Input v-model="form.category" placeholder="e.g. Sci-Fi" />
            </div>
            <div class="grid gap-2">
              <Label>Ambiance</Label>
              <Input v-model="form.ambiance" placeholder="e.g. Dark, Neon" />
            </div>
          </div>

          <div class="grid gap-2">
            <Label>Theme Keywords</Label>
            <Textarea 
              v-model="form.keywords_theme" 
              placeholder="e.g. neon lights, rain, skyscrapers" 
              class="h-20"
            />
          </div>

          <div class="grid gap-2">
            <Label>Background Prompt</Label>
            <Textarea 
              v-model="form.prompt_background" 
              placeholder="Full background description..." 
              class="h-24"
            />
          </div>

          <div class="grid gap-2">
            <Label>Integration Idea</Label>
            <Textarea 
              v-model="form.integration_idea" 
              placeholder="How the character fits in..." 
              class="h-20"
            />
          </div>
        </div>

        <DialogFooter>
          <Button @click="handleSubmit" :disabled="isSubmitting">
            {{ isSubmitting ? 'Saving...' : 'Save Theme' }}
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
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { useThemesList, useCreateTheme, useUpdateTheme, useDeleteTheme } from '@/lib/api-client'
import type { Theme } from '@/api'

const { data: themes, isLoading } = useThemesList()

const { mutateAsync: createTheme, isPending: isCreating } = useCreateTheme()
const { mutateAsync: updateTheme, isPending: isUpdating } = useUpdateTheme()
const { mutate: deleteTheme } = useDeleteTheme()

const isDialogOpen = ref(false)
const editingId = ref<number | null>(null)
const isEditing = computed(() => !!editingId.value)
const isSubmitting = computed(() => isCreating.value || isUpdating.value)

const form = reactive({
  name: '',
  category: '',
  ambiance: '',
  keywords_theme: '',
  prompt_background: '',
  integration_idea: ''
})

const openCreateDialog = () => {
  editingId.value = null
  form.name = ''
  form.category = ''
  form.ambiance = ''
  form.keywords_theme = ''
  form.prompt_background = ''
  form.integration_idea = ''
  isDialogOpen.value = true
}

const openEditDialog = (theme: Theme) => {
  editingId.value = theme.id!
  form.name = theme.name
  form.category = theme.category || ''
  form.ambiance = theme.ambiance || ''
  form.keywords_theme = theme.keywords_theme || ''
  form.prompt_background = theme.prompt_background || ''
  form.integration_idea = theme.integration_idea || ''
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
      category: form.category,
      ambiance: form.ambiance,
      keywords_theme: form.keywords_theme,
      prompt_background: form.prompt_background,
      integration_idea: form.integration_idea
    }

    if (isEditing.value && editingId.value) {
      await updateTheme({ id: editingId.value, ...payload })
    } else {
      await createTheme(payload)
    }
    isDialogOpen.value = false
  } catch (error) {
    console.error(error)
    alert('Failed to save theme')
  }
}

const handleDelete = (id: number) => {
  if (confirm('Are you sure you want to delete this theme?')) {
    deleteTheme(id)
  }
}
</script>
