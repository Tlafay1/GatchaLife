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

    <!-- CREATION MODE: Simple Entry -->
    <Card v-if="!isEditMode">
      <CardHeader>
        <CardTitle>New Character Entry</CardTitle>
        <CardDescription>Start by providing the basic identity and source material.</CardDescription>
      </CardHeader>
      <CardContent class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2">
            <Label>Character Name</Label>
            <Input v-model="form.name" placeholder="e.g. Sylphiette" />
          </div>

          <!-- Series Selection -->
          <div class="space-y-2">
            <Label>Series Source</Label>
            <div class="flex gap-2">
              <Select v-model="form.series">
                <SelectTrigger class="w-full">
                  <SelectValue placeholder="Select a series" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem v-if="isLoadingSeries" value="loading" disabled>Loading...</SelectItem>
                  <SelectItem v-for="s in seriesList" :key="s.id" :value="String(s.id)">
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
                      <Textarea v-model="newSeriesDescription" class="col-span-3 h-24 resize-none"
                        placeholder="Optional description for this series..." />
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
          <Label>Identity Face Image</Label>
          <div class="flex items-center gap-4">
            <div v-if="form.identity_face_image_url" class="relative group w-16 h-16 rounded-md overflow-hidden border">
              <img :src="form.identity_face_image_url" class="w-full h-full object-cover" />
            </div>
            <Input type="file" accept="image/*" @change="handleFaceImageUpload" />
          </div>
        </div>

        <div class="space-y-2">
          <Label>Wiki Source Text</Label>
          <Textarea v-model="form.wiki_source_text" class="min-h-[200px] font-mono text-xs"
            placeholder="Paste raw wiki text here (this will be sent to the automation pipeline)..." />
          <p class="text-xs text-muted-foreground">This text will be parsed by the AI to autofill details later.</p>
        </div>
      </CardContent>
    </Card>

    <!-- EDIT MODE: Full Details -->
    <div v-else class="space-y-6">

      <!-- Core Identity -->
      <Card>
        <CardHeader>
          <CardTitle>Core Identity</CardTitle>
          <CardDescription>Universal traits applied to all variants.</CardDescription>
        </CardHeader>
        <CardContent class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="space-y-2">
              <Label>Character Name</Label>
              <Input v-model="form.name" />
            </div>
            <div class="space-y-2">
              <Label>Series Source</Label>
              <Select v-model="form.series">
                <SelectTrigger class="w-full">
                  <SelectValue placeholder="Select a series" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem v-for="s in seriesList" :key="s.id" :value="String(s.id)">
                    {{ s.name }}
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div class="space-y-2">
            <Label>Base Description</Label>
            <Textarea v-model="form.base_description" class="min-h-[100px]" />
          </div>

          <div class="space-y-2">
            <Label>Unlock Level</Label>
            <Input v-model="form.unlock_level" type="number" min="1" />
          </div>
        </CardContent>
      </Card>

      <!-- Technical Details -->
      <Card>
        <CardHeader>
          <CardTitle>Technical Guidance</CardTitle>
          <CardDescription>Detailed attributes for Generative AI consistency.</CardDescription>
        </CardHeader>
        <CardContent class="space-y-6">
          <!-- Physical Appearance -->
          <div class="space-y-4">
            <h3 class="text-sm font-medium text-foreground">Physical Appearance</h3>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-2">
                <Label>Identity Face Image</Label>
                <div class="flex items-center gap-4">
                  <div v-if="form.identity_face_image_url"
                    class="relative group w-16 h-16 rounded-md overflow-hidden border">
                    <img :src="form.identity_face_image_url" class="w-full h-full object-cover" />
                  </div>
                  <Input type="file" accept="image/*" @change="handleFaceImageUpload" />
                </div>
              </div>
              <div class="space-y-2">
                <Label>Height Perception</Label>
                <Select v-model="form.height_perception">
                  <SelectTrigger>
                    <SelectValue placeholder="Select Height" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="SHORT">Short</SelectItem>
                    <SelectItem value="AVERAGE">Average</SelectItem>
                    <SelectItem value="TALL">Tall</SelectItem>
                    <SelectItem value="GIANT">Giant</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div class="space-y-2">
              <Label>Body Type Description</Label>
              <Input v-model="form.body_type_description" placeholder="ex: petite stature, slender build" />
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="space-y-2">
                <Label>Hair Prompt</Label>
                <Textarea v-model="form.hair_prompt" class="h-20" placeholder="Visual description of hair" />
              </div>
              <div class="space-y-2">
                <Label>Eye Prompt</Label>
                <Textarea v-model="form.eye_prompt" class="h-20" placeholder="Visual description of eyes" />
              </div>
            </div>

            <div class="space-y-2">
              <Label>Visual Traits (JSON List)</Label>
              <Textarea v-model="form.visual_traits" class="h-20 font-mono text-xs"
                placeholder="['scar on left eye', 'pale skin']" />
              <p class="text-xs text-muted-foreground">Enter as a valid JSON array of strings.</p>
            </div>
          </div>

          <!-- Personality & Environment -->
          <div class="space-y-4 pt-4 border-t">
            <h3 class="text-sm font-medium text-foreground">Personality & Lore context</h3>

            <div class="space-y-2">
              <Label>Lore Tags (JSON List)</Label>
              <Textarea v-model="form.lore_tags" class="h-16 font-mono text-xs"
                placeholder="['stealth', 'modern', 'cynical']" />
            </div>

            <div class="space-y-2">
              <Label>Affinity Environments (JSON List of Objects)</Label>
              <Textarea v-model="form.affinity_environments" class="h-24 font-mono text-xs"
                placeholder="[{'name': 'shadows', 'visual_prompt': 'dark alley'}]" />
            </div>

            <div class="space-y-2">
              <Label>Clashing Environments (JSON List)</Label>
              <Textarea v-model="form.clashing_environments" class="h-16 font-mono text-xs"
                placeholder="['holy church', 'bright beach']" />
            </div>

            <div class="space-y-2">
              <Label>Negative Traits Suggestion</Label>
              <Textarea v-model="form.negative_traits_suggestion" placeholder="Negative prompt morphologique" />
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- Visual Variants -->
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <h2 class="text-xl font-semibold tracking-tight">Visual Variants</h2>
          <Button variant="outline" size="sm" @click="addVariant">
            <Plus class="w-4 h-4 mr-2" /> Add Variant
          </Button>
        </div>

        <div v-if="form.variants.length === 0"
          class="flex flex-col items-center justify-center py-12 border-2 border-dashed rounded-lg bg-muted/30">
          <div class="text-muted-foreground mb-2">No variants defined</div>
          <Button variant="link" @click="addVariant">Create your first variant</Button>
        </div>

        <VariantItem v-for="(variant, index) in form.variants" :key="variant.id || `new-${index}`"
          :model-value="variant" @update:model-value="(newVal) => form.variants[index] = newVal"
          @remove="removeVariant(index)" :onScheduleImageForDeletion="scheduleImageForDeletion" />
      </div>

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
  useUploadVariantImage, useDeleteVariantImage,
  useUploadCharacterFace
} from '@/lib/api-client'
import type { CharacterFormState } from '@/types/gacha'

const props = defineProps<{ id?: string }>()
const router = useRouter()
const queryClient = useQueryClient()

const isEditMode = computed(() => !!props.id)

// --- FORM STATE ---
type LocalFormState = Omit<CharacterFormState, 'visual_traits' | 'lore_tags' | 'affinity_environments' | 'clashing_environments'> & {
  visual_traits: string;
  lore_tags: string;
  affinity_environments: string;
  clashing_environments: string;
  wiki_source_text?: string;
  identity_face_image_url?: string | null;
}

const form = reactive<LocalFormState>({
  name: '',
  series: '',
  base_description: '',
  variants: [],
  unlock_level: 1,

  // New Fields
  wiki_source_text: '',
  identity_face_image: null,
  identity_face_image_url: null,
  body_type_description: '',
  height_perception: '', // Defaults to empty string, mapped to Enum
  hair_prompt: '',
  eye_prompt: '',

  // Storing JSON as strings for Textarea editing
  visual_traits: '[]',
  lore_tags: '[]',
  affinity_environments: '[]',
  clashing_environments: '[]',
  negative_traits_suggestion: ''
})

const variantsToDelete = ref<number[]>([])
const imagesToDelete = ref<number[]>([])

// --- DATA FETCHING (for edit mode) ---
const { data: characterData } = useCharacterDetails(parseInt(props.id || '0'))

watch(characterData, (newChar) => {
  if (newChar) {
    form.name = newChar.name || ''
    form.series = String(newChar.series as number)
    form.base_description = newChar.description || ''
    form.unlock_level = newChar.unlock_level || 1

    // New Fields Mapping
    form.identity_face_image_url = newChar.identity_face_image || null
    form.body_type_description = newChar.body_type_description || ''
    form.height_perception = (newChar.height_perception as any) || ''
    form.hair_prompt = newChar.hair_prompt || ''
    form.eye_prompt = newChar.eye_prompt || ''
    form.visual_traits = JSON.stringify(newChar.visual_traits || [], null, 2)
    form.lore_tags = JSON.stringify(newChar.lore_tags || [], null, 2)
    form.affinity_environments = JSON.stringify(newChar.affinity_environments || [], null, 2)
    form.clashing_environments = JSON.stringify(newChar.clashing_environments || [], null, 2)
    form.negative_traits_suggestion = newChar.negative_traits_suggestion || ''

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
const { mutateAsync: uploadImage, isPending: isUploadingVariantImg } = useUploadVariantImage()
const { mutateAsync: deleteImage } = useDeleteVariantImage()
const { mutateAsync: uploadFace, isPending: isUploadingFace } = useUploadCharacterFace()

const isSaving = computed(() => isUpdatingChar.value || isUpdatingVariant.value)
const isUploading = computed(() => isUploadingVariantImg.value || isUploadingFace.value)
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

const scheduleImageForDeletion = (id: number) => {
  imagesToDelete.value.push(id)
}

const handleFaceImageUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    form.identity_face_image = target.files[0]
    // Preview
    form.identity_face_image_url = URL.createObjectURL(target.files[0])
  }
}

// --- SUBMISSION LOGIC ---
const onSubmit = async () => {
  if (!form.series || !form.name) {
    alert("Name and Series are required.")
    return
  }

  // Parse JSON Helpers
  const parseJson = (str: string, fieldName: string) => {
    try {
      return JSON.parse(str)
    } catch (e) {
      alert(`Invalid JSON in ${fieldName}\n\n${e}`)
      throw e
    }
  }

  try {
    let charId: number

    if (isEditMode.value) {
      console.log("Step 1: Updating Character")

      const payload: any = {
        id: parseInt(props.id!),
        name: form.name,
        series: parseInt(form.series),
        description: form.base_description,
        unlock_level: form.unlock_level,
        // New Fields
        body_type_description: form.body_type_description,
        height_perception: form.height_perception || null,
        hair_prompt: form.hair_prompt,
        eye_prompt: form.eye_prompt,
        negative_traits_suggestion: form.negative_traits_suggestion,

        visual_traits: parseJson(form.visual_traits || '[]', 'Visual Traits'),
        lore_tags: parseJson(form.lore_tags || '[]', 'Lore Tags'),
        affinity_environments: parseJson(form.affinity_environments || '[]', 'Affinity Environments'),
        clashing_environments: parseJson(form.clashing_environments || '[]', 'Clashing Environments'),
      }

      const updated = await updateCharacter(payload)
      charId = updated.id!

      // Handle Face Image Upload
      if (form.identity_face_image) {
        await uploadFace({ characterId: charId, file: form.identity_face_image })
      }

    } else {
      console.log("Step 1: Creating Character")
      // Creation passes wiki_source_text via extra parameter
      const payload: any = {
        name: form.name,
        series: parseInt(form.series),
        // Wiki text for automation
        wiki_source_text: form.wiki_source_text
      }

      const newChar = await createCharacter(payload)
      charId = newChar.id!

      // Handle Face Image Upload for creation
      if (form.identity_face_image) {
        console.log("Step 1b: Uploading Face Image")
        await uploadFace({ characterId: charId, file: form.identity_face_image })
      }
    }

    // Common Steps (Deletion and Variants) Only run in edit mode effectively, but creation might have variants if we allowed it (we hid it in UI)
    if (isEditMode.value) {
      // Step 2: Process Deletions
      console.log("Step 2: Processing Deletions")
      await Promise.all([
        ...variantsToDelete.value.map(id => deleteVariant({ id, characterId: charId })),
        ...imagesToDelete.value.map(id => deleteImage(id))
      ])

      // Step 3: Process Variants
      console.log("Step 3: Processing Variants")
      await Promise.all(form.variants.map(async (variant) => {
        let variantId: number
        const variantPayload = {
          character: charId,
          name: variant.name,
          description: variant.visual_description
        }

        if (variant.id) { // Update
          const updatedVar = await updateVariant({ id: variant.id, ...variantPayload })
          variantId = updatedVar.id!
        } else { // Create
          const newVar = await createVariant(variantPayload)
          variantId = newVar.id!
        }

        // Step 4: Process Images
        await Promise.all(variant.images.map(img => {
          if (img.file && img.is_new) {
            return uploadImage({
              variantId: variantId,
              file: img.file,
            })
          }
        }))
      }))
    }

    // Finalization
    await queryClient.invalidateQueries({ queryKey: ['character', charId] })
    alert(`Character ${isEditMode.value ? 'updated' : 'forged'} successfully!`)
    router.push('/')

  } catch (error) {
    console.error("Operation Failed:", error)
  }
}

defineExpose({ form })
</script>
