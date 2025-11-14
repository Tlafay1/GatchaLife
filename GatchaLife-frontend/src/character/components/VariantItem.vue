<template>
  <Card class="mb-6 relative border-dashed border-2 hover:border-solid transition-colors bg-card text-card-foreground">
    <CardHeader class="pb-3">
      <div class="flex justify-between items-center">
        <CardTitle class="text-base font-medium flex items-center gap-2">
          <span class="bg-primary/10 text-primary px-2 py-1 rounded text-xs uppercase tracking-wide">
            {{ modelValue.name || 'New Variant' }}
          </span>
        </CardTitle>
        <Button 
          variant="ghost" 
          size="sm" 
          class="text-destructive hover:bg-destructive/10 h-8"
          @click="$emit('remove')"
        >
          <Trash2 class="w-4 h-4 mr-2" /> Remove
        </Button>
      </div>
    </CardHeader>

    <CardContent class="grid gap-4">
      <div class="space-y-2">
        <Label>Variant Name</Label>
        <Input 
          :model-value="modelValue.name" 
          @update:model-value="(v) => updateField('name', v as string)"
          placeholder="e.g. Academy Arc / Young Version" 
        />
      </div>

      <div class="space-y-2">
        <Label>Visual Prompt Details</Label>
        <Textarea 
          :model-value="modelValue.visual_description" 
          @update:model-value="(v) => updateField('visual_description', v as string)"
          placeholder="Describe hair, eyes, clothing specific to this version..."
          class="h-24 resize-none"
        />
      </div>

      <Separator class="my-2" />

      <div class="space-y-3">
        <div class="flex justify-between items-end">
          <Label>Reference Images (Dataset)</Label>
          <span class="text-xs text-muted-foreground">{{ (modelValue.images || []).length }} images loaded</span>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
          <label 
            class="flex flex-col items-center justify-center h-32 border-2 border-dashed border-muted-foreground/25 rounded-md cursor-pointer hover:bg-accent/50 transition-colors"
          >
            <Upload class="w-6 h-6 text-muted-foreground mb-2" />
            <span class="text-xs text-muted-foreground font-medium">Add Images</span>
            <input type="file" multiple @change="handleFiles" class="hidden" accept="image/*" />
          </label>

          <div 
            v-for="(imgObj, idx) in modelValue.images" 
            :key="idx" 
            class="group relative h-32 rounded-md overflow-hidden border bg-muted"
          >
            <img :src="getPreview(imgObj)" class="w-full h-full object-cover opacity-90 group-hover:opacity-100 transition-opacity" alt="preview" />
            
            <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-between p-2">
              <div class="flex justify-end">
                <Button 
                  variant="destructive" 
                  size="icon" 
                  class="h-6 w-6 rounded-full"
                  @click.stop="removeImage(idx)"
                >
                  <X class="w-3 h-3" />
                </Button>
              </div>
              
              <select 
                :value="imgObj.view_type"
                @change="(e) => updateViewType(idx, (e.target as HTMLSelectElement).value as ViewType)"
                class="w-full text-[10px] h-6 rounded bg-background/90 border-none px-1 focus:ring-1 focus:ring-primary text-foreground"
                @click.stop
              >
                <option value="front">Front</option>
                <option value="side">Side</option>
                <option value="action">Action</option>
                <option value="detail">Detail</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup lang="ts">
import { Trash2, Upload, X } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'
import type { LocalVariantForm, LocalVariantImage, ViewType } from '@/types/gacha'

const props = defineProps<{
  modelValue: LocalVariantForm
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: LocalVariantForm): void
  (e: 'remove'): void
}>()

const updateField = (field: keyof LocalVariantForm, value: string) => {
  emit('update:modelValue', {
    ...props.modelValue,
    [field]: value
  })
}

const updateViewType = (idx: number, type: ViewType) => {
  const newImages = [...props.modelValue.images]
  newImages[idx] = { ...newImages[idx], view_type: type }
  emit('update:modelValue', { ...props.modelValue, images: newImages })
}

const getPreview = (imgObj: LocalVariantImage) => {
  if (imgObj.file instanceof File) return URL.createObjectURL(imgObj.file)
  return imgObj.url || ''
}

const handleFiles = (e: Event) => {
  const input = e.target as HTMLInputElement
  if (!input.files) return

  const newFiles = Array.from(input.files).map(f => ({
    file: f,
    view_type: 'front' as ViewType,
    is_new: true
  }))

  emit('update:modelValue', {
    ...props.modelValue,
    images: [...props.modelValue.images, ...newFiles]
  })
}

const removeImage = (index: number) => {
  const updatedImages = [...props.modelValue.images]
  updatedImages.splice(index, 1)
  emit('update:modelValue', { ...props.modelValue, images: updatedImages })
}
</script>