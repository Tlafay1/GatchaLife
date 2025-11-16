<template>
  <div class="max-w-4xl mx-auto p-6 space-y-8">
    
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">{{ isEditMode ? 'Edit Character' : 'Character Forge' }}</h1>
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
        :key="variant.id || `new-${index}`"
        v-model="form.variants[index]"
        @remove="removeVariant(index)"
        :onScheduleImageForDeletion="scheduleImageForDeletion"
      />
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, Save } from 'lucide-vue-next'
import { useQueryClient } from '@tanstack/vue-query'

// UI Components
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import VariantItem from '@/character/components/VariantItem.vue'

// API and Types
import {
  useSeriesList, useCreateSeries, useCharacterDetails,
  useCreateCharacter, useUpdateCharacter,
  useCreateVariant, useUpdateVariant, useDeleteVariant,
  useUploadVariantImage, useDeleteVariantImage
} from '@/lib/api-client'
import type { CharacterFormState, LocalVariantForm, LocalVariantImage } from '@/types/gacha'

const props = defineProps<{ id?: string }>()
const router = useRouter()
const queryClient = useQueryClient()

const isEditMode = computed(() => !!props.id)

// --- FORM STATE ---
const form = reactive<CharacterFormState>({
  name: '',
  series: '',
  base_description: '',
  variants: []
})
const variantsToDelete = ref<number[]>([])
const imagesToDelete = ref<number[]>([])

// --- DATA FETCHING (for edit mode) ---
const { data: characterData, isLoading: isLoadingCharacter } = useCharacterDetails(parseInt(props.id || ''))

watch(characterData, (newChar) => {
  if (newChar) {
    form.name = newChar.name || ''
    form.series = String(newChar.series as number)
    form.base_description = newChar.description || ''
    form.variants = (newChar.variants || []).map(v => ({
      id: v.id,
      name: v.name || '',
      visual_description: v.description || '',
      images: (v.images || []).map(img => ({
        id: img.id,
        url: img.image,
      }))
    }))
  }
}, { immediate: true })

// --- SERIES LOGIC ---
const { data: seriesList, isLoading: isLoadingSeries } = useSeriesList()
const { mutateAsync: createSeries, isPending: isCreatingSeries } = useCreateSeries()
const isSeriesDialogOpen = ref(false)
const newSeriesName = ref('')
const newSeriesDescription = ref('')

const handleCreateSeries = async () => {
  if (!newSeriesName.value) return
  const newItem = await createSeries({ name: newSeriesName.value, description: newSeriesDescription.value })
  if (newItem) {
    form.series = String(newItem.id)
    isSeriesDialogOpen.value = false
    newSeriesName.value = ''
    newSeriesDescription.value = ''
  }
}

// --- MUTATIONS ---
const { mutateAsync: createCharacter } = useCreateCharacter()
const { mutateAsync: updateCharacter, isPending: isUpdatingChar } = useUpdateCharacter()
const { mutateAsync: createVariant } = useCreateVariant()
const { mutateAsync: updateVariant, isPending: isUpdatingVariant } = useUpdateVariant()
const { mutateAsync: deleteVariant } = useDeleteVariant()
const { mutateAsync: uploadImage, isPending: isUploading } = useUploadVariantImage()
const { mutateAsync: deleteImage } = useDeleteVariantImage()

const isSaving = computed(() => isUpdatingChar.value || isUpdatingVariant.value)
const buttonLabel = computed(() => {
  if (isEditMode.value) {
    return isSaving.value ? 'Saving...' : 'Save Changes'
  }
  return isSaving.value ? 'Forging...' : 'Save Character'
})

// --- FORM ACTIONS ---
const addVariant = () => {
  form.variants.push({ name: '', visual_description: '', images: [] })
}

const removeVariant = (index: number) => {
  const variant = form.variants[index]
  if (variant?.id) {
    variantsToDelete.value.push(variant.id)
  }
  form.variants.splice(index, 1)
}

// This function needs to be passed down to VariantItem component
const scheduleImageForDeletion = (id: number) => {
  imagesToDelete.value.push(id)
}

// --- SUBMISSION LOGIC ---
const onSubmit = async () => {
  if (!form.series || !form.name) {
    alert("Name and Series are required.")
    return
  }

  try {
    let charId: number
    
    // Step 1: Create or Update Character
    if (isEditMode.value) {
      console.log("Step 1: Updating Character")
      const updated = await updateCharacter({
        id: parseInt(props.id!),
        name: form.name,
        series: parseInt(form.series),
        description: form.base_description
      })
      charId = updated.id!
    } else {
      console.log("Step 1: Creating Character")
      const newChar = await createCharacter({
        name: form.name,
        series: parseInt(form.series),
        description: form.base_description
      })
      charId = newChar.id!
    }

    // Step 2: Process Deletions
    console.log("Step 2: Processing Deletions")
    await Promise.all([
      ...variantsToDelete.value.map(id => deleteVariant({ id, characterId: charId })),
      ...imagesToDelete.value.map(id => deleteImage(id))
    ])

    // Step 3: Process Variants (Create/Update)
    console.log("Step 3: Processing Variants")
    await Promise.all(form.variants.map(async (variant) => {
      let variantId: number
      const variantPayload = {
        character: charId,
        name: variant.name,
        description: variant.visual_description
      }

      if (variant.id) { // Update existing variant
        const updatedVar = await updateVariant({ id: variant.id, ...variantPayload })
        variantId = updatedVar.id!
      } else { // Create new variant
        const newVar = await createVariant(variantPayload)
        variantId = newVar.id!
      }

      // Step 4: Process Images for this variant
      await Promise.all(variant.images.map(img => {
        if (img.file && img.is_new) {
          return uploadImage({
            variantId: variantId,
            file: img.file,
          })
        }
      }))
    }))

    // Finalization
    await queryClient.invalidateQueries({ queryKey: ['character', charId] })
    alert(`Character ${isEditMode.value ? 'updated' : 'forged'} successfully!`)
    router.push('/')

  } catch (error) {
    console.error("Operation Failed:", error)
    alert("An error occurred. Check the console for details.")
  }
}
</script>
