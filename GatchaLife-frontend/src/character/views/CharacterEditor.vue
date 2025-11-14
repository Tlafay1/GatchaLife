<template>
  <div class="max-w-4xl mx-auto p-6 space-y-8">
    
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Character Forge</h1>
        <p class="text-muted-foreground">Define entities for AI generation rewards.</p>
      </div>
      <Button @click="onSubmit" :disabled="isSaving || isUploading">
        <Save class="w-4 h-4 mr-2" />
        {{ buttonLabel }}
      </Button>
    </div>

    <Card>
      <CardHeader>
        <CardTitle>Core Identity</CardTitle>
        <CardDescription>Universal traits applied to all variants.</CardDescription>
      </CardHeader>
      <CardContent class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2">
            <Label>Character Name</Label>
            <Input v-model="form.name" placeholder="e.g. Sylphiette" />
          </div>
          
          <div class="space-y-2">
            <Label>Series Source</Label>
            <div class="flex gap-2">
              <Select v-model="form.series">
                <SelectTrigger class="w-full">
                  <SelectValue placeholder="Select a series" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem v-if="isLoadingSeries" value="loading" disabled>Loading...</SelectItem>
                  <SelectItem 
                    v-for="s in seriesList" 
                    :key="s.id" 
                    :value="String(s.id)"
                  >
                    {{ s.name }}
                  </SelectItem>
                </SelectContent>
              </Select>
              
              <Dialog v-model:open="isSeriesDialogOpen">
                <DialogTrigger as-child>
                  <Button variant="outline" size="icon" title="Add New Series">
                    <Plus class="h-4 w-4" />
                  </Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Create New Series</DialogTitle>
                    <DialogDescription>Add a new show or universe to your database.</DialogDescription>
                  </DialogHeader>
                  <div class="grid gap-4 py-4">
                    <div class="grid grid-cols-4 items-center gap-4">
                      <Label class="text-right">Name</Label>
                      <Input v-model="newSeriesName" class="col-span-3" placeholder="e.g. Mushoku Tensei" />
                    </div>
                    <div class="grid grid-cols-4 items-center gap-4">
                      <Label class="text-right">Description</Label>
                      <Textarea 
                        v-model="newSeriesDescription" 
                        class="col-span-3 h-24 resize-none"
                        placeholder="Optional description for this series..."
                      />
                    </div>
                  </div>
                  <DialogFooter>
                    <Button @click="handleCreateSeries" :disabled="isCreatingSeries">
                      {{ isCreatingSeries ? 'Creating...' : 'Create Series' }}
                    </Button>
                  </DialogFooter>
                </DialogContent>
              </Dialog>
            </div>
          </div>
        </div>

        <div class="space-y-2">
          <Label>Base Description</Label>
          <Textarea 
            v-model="form.base_description" 
            class="min-h-[100px]"
            placeholder="Core traits: species, gender, personality, key features..."
          />
        </div>
      </CardContent>
    </Card>

    <div class="space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-semibold tracking-tight">Visual Variants</h2>
        <Button variant="outline" size="sm" @click="addVariant">
          <Plus class="w-4 h-4 mr-2" /> Add Variant
        </Button>
      </div>

      <div v-if="form.variants.length === 0" class="flex flex-col items-center justify-center py-12 border-2 border-dashed rounded-lg bg-muted/30">
        <div class="text-muted-foreground mb-2">No variants defined</div>
        <Button variant="link" @click="addVariant">Create your first variant</Button>
      </div>

      <VariantItem 
        v-for="(variant, index) in form.variants" 
        :key="index"
        v-model="form.variants[index]"
        @remove="removeVariant(index)"
      />
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { Plus, Save } from 'lucide-vue-next'

// UI Components
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'

import VariantItem from '@/character/components/VariantItem.vue'

// Types & API
import type { CharacterFormState, ViewType } from '@/types/gacha'
import { CharactersService, SeriesService, VariantsService } from '@/api'
import type { Character, CharacterVariant, Series } from '@/api'

const queryClient = useQueryClient()

// --- FORM STATE ---
const form = reactive<CharacterFormState>({
  name: '',
  series: '',
  base_description: '',
  variants: []
})

// --- SERIES LOGIC ---
const { data: seriesList, isLoading: isLoadingSeries } = useQuery<Series[]>({
  queryKey: ['series'],
  queryFn: () => SeriesService.seriesList(),
})

const isSeriesDialogOpen = ref(false)
const newSeriesName = ref('')
const newSeriesDescription = ref('')

const { mutateAsync: createSeries, isPending: isCreatingSeries } = useMutation({
  mutationFn: (data: { name: string, description: string }) => SeriesService.seriesCreate(data),
  onSuccess: (newItem) => {
    queryClient.invalidateQueries({ queryKey: ['series'] })
    form.series = String(newItem.id)
    isSeriesDialogOpen.value = false
    newSeriesName.value = ''
    newSeriesDescription.value = ''
  }
})

const handleCreateSeries = async () => {
  if (!newSeriesName.value) return
  await createSeries({ name: newSeriesName.value, description: newSeriesDescription.value })
}

// --- MAIN LOGIC ---

// 1. Create Character
const { mutateAsync: createCharacter, isPending: isSavingChar } = useMutation({
  mutationFn: (data: { name: string, series: number, description: string }) => 
    CharactersService.charactersCreate(data)
})

// 2. Create Variant
const { mutateAsync: createVariant, isPending: isSavingVariant } = useMutation({
  mutationFn: (data: { character: number, name: string, description: string }) => 
    VariantsService.variantsCreate(data)
})

// 3. Upload Image (Manual Fetch)
const { mutateAsync: uploadImage, isPending: isUploading } = useMutation({
  mutationFn: async ({ variantId, file, viewType }: { variantId: number, file: File, viewType: ViewType }) => {
    const formData = new FormData()
    formData.append('variant', String(variantId))
    formData.append('image', file)
    
    // Note: Your django model snippet removed 'view_type', but we send it in case 
    // you add it back to models.py. Django will simply ignore it if not in the Form.
    formData.append('view_type', viewType) 

    // Adjust URL to your actual API endpoint
    const response = await fetch('http://127.0.0.1:8000/variant-images/', {
      method: 'POST',
      body: formData,
      // Do NOT set Content-Type header manually; fetch does it for FormData
    })

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`)
    }
    return response.json()
  }
})

const isSaving = computed(() => isSavingChar.value || isSavingVariant.value)
const buttonLabel = computed(() => {
  if (isSavingChar.value) return 'Forging Character...'
  if (isSavingVariant.value) return 'Creating Variants...'
  if (isUploading.value) return 'Uploading Reference Data...'
  return 'Save Character'
})

const addVariant = () => {
  form.variants.push({
    name: '',
    visual_description: '', // Maps to description in DB
    images: []
  })
}

const removeVariant = (index: number) => {
  form.variants.splice(index, 1)
}

const onSubmit = async () => {
  if (!form.series || !form.name) {
    alert("Name and Series are required.")
    return
  }

  try {
    // Step 1: Create Character
    console.log("Step 1: Creating Character")
    const charData: Character = await createCharacter({
      name: form.name,
      series: parseInt(form.series),
      description: form.base_description
    })
    
    // Step 2: Loop Variants
    console.log(`Step 2: Creating ${form.variants.length} variants for Char ID ${charData.id}`)
    
    await Promise.all(form.variants.map(async (variant) => {
      const varData: CharacterVariant = await createVariant({
        character: charData.id!,
        name: variant.name,
        description: variant.visual_description
      })
      
      // Step 3: Loop Images
      if (variant.images.length > 0) {
        console.log(`Step 3: Uploading ${variant.images.length} images for Variant ID ${varData.id}`)
        await Promise.all(variant.images.map(img => {
          if (img.file) {
            return uploadImage({
              variantId: varData.id!,
              file: img.file,
              viewType: img.view_type
            })
          }
        }))
      }
    }))

    alert("Character Forged Successfully!")
    // Reset form or redirect logic here

  } catch (error) {
    console.error("Forging Failed:", error)
    alert("Error saving character. Check console.")
  }
}
</script>