<template>
  <Card class="mb-6 relative border-dashed border-2 hover:border-solid transition-colors bg-card text-card-foreground">
    <CardHeader class="pb-3">
      <div class="flex justify-between items-center">
        <CardTitle class="text-base font-medium flex items-center gap-3">
          <span class="bg-primary/10 text-primary px-2 py-1 rounded text-xs uppercase tracking-wide font-bold">
            {{ modelValue.name || 'New Variant' }}
          </span>
          <span 
            v-if="modelValue.variant_type" 
            :class="[
              'px-2 py-0.5 rounded-full text-[10px] uppercase tracking-wider border',
              modelValue.variant_type === 'CANON' ? 'border-amber-500/50 text-amber-600 bg-amber-500/10' : 'border-blue-500/50 text-blue-600 bg-blue-500/10'
            ]"
          >
            {{ modelValue.variant_type }}
          </span>
        </CardTitle>
      <div class="flex items-center gap-3">
        <div class="flex items-center space-x-2 border px-2 py-1 rounded bg-background/50">
          <input 
            type="checkbox" 
            :id="`legacy-variant-${modelValue.id || 'new'}`" 
            :checked="modelValue.legacy" 
            @change="(e) => updateField('legacy', (e.target as HTMLInputElement).checked)"
            class="h-3 w-3 rounded border-input" 
          />
          <Label :for="`legacy-variant-${modelValue.id || 'new'}`" class="text-xs cursor-pointer">Archived</Label>
        </div>
        <Button 
          variant="ghost" 
          size="sm" 
          class="text-destructive hover:bg-destructive/10 h-8"
          @click="$emit('remove')"
        >
          <Trash2 class="w-4 h-4 mr-2" /> Remove
        </Button>
      </div>
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
        <Label>Narrative Description</Label>
        <Textarea 
          :model-value="modelValue.description" 
          @update:model-value="(v) => updateField('description', v as string)"
          placeholder="Narrative description of this variant..."
          class="h-20 resize-none text-sm"
        />
      </div>

      <div class="space-y-2 bg-muted/30 p-3 rounded-md border border-muted/50">
        <Label class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Technical Visual Override (AI)</Label>
        <Textarea 
          :model-value="modelValue.visual_override" 
          @update:model-value="(v) => updateField('visual_override', v as string)"
          placeholder="Technical prompt for image generation..."
          class="h-24 resize-none font-mono text-xs mt-1"
        />
      </div>
      
      <div v-if="modelValue.card_configurations && modelValue.card_configurations.length" class="space-y-2">
        <Label class="text-xs text-muted-foreground">Generated Card Configurations</Label>
        <div class="border rounded-md overflow-hidden text-xs">
          <div class="grid grid-cols-12 gap-2 bg-muted/50 p-2 font-medium border-b">
            <div class="col-span-2">Rarity</div>
            <div class="col-span-3">Theme</div>
            <div class="col-span-3">Style</div>
            <div class="col-span-3">Pose</div>
            <div class="col-span-1 text-center">Legacy</div>
          </div>
          <div v-for="(config, idx) in modelValue.card_configurations" :key="idx" 
               :class="['grid grid-cols-12 gap-2 p-2 border-b last:border-0 hover:bg-muted/20 items-center', config.legacy ? 'opacity-50 grayscale bg-muted/30' : '']">
            <div class="col-span-2">
              <span :class="['px-1.5 py-0.5 rounded text-[10px] uppercase font-bold border', 
                config.rarity === 'COMMON' ? 'bg-slate-100 text-slate-600 border-slate-200' :
                config.rarity === 'RARE' ? 'bg-blue-100 text-blue-600 border-blue-200' :
                'bg-yellow-100 text-yellow-600 border-yellow-200'
              ]">{{ config.rarity }}</span>
            </div>
            <div class="col-span-3 font-medium truncate" :title="config.theme?.name">{{ config.theme?.name || '-' }}</div>
            <div class="col-span-3 truncate" :title="config.style?.name">{{ config.style?.name || '-' }}</div>
            <div class="col-span-3 text-muted-foreground truncate italic" :title="config.pose">{{ config.pose || '-' }}</div>
            <div class="col-span-1 flex justify-center">
               <input 
                 type="checkbox" 
                 :checked="config.legacy" 
                 @change="toggleConfigLegacy(idx)"
                 class="h-3 w-3 rounded border-input cursor-pointer"
                 title="Archive this configuration"
               />
            </div>
          </div>
        </div>
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
import type { LocalVariantForm, LocalVariantImage } from '@/types/gacha'

const props = defineProps<{
  modelValue: LocalVariantForm
  onScheduleImageForDeletion: (id: number) => void
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: LocalVariantForm): void
  (e: 'remove'): void
}>()

const updateField = (field: keyof LocalVariantForm, value: string | boolean) => {
  emit('update:modelValue', {
    ...props.modelValue,
    [field]: value
  })
}

const toggleConfigLegacy = (index: number) => {
  const configs = [...props.modelValue.card_configurations]
  configs[index] = { ...configs[index], legacy: !configs[index].legacy }
  emit('update:modelValue', { ...props.modelValue, card_configurations: configs })
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
    is_new: true
  }))

  emit('update:modelValue', {
    ...props.modelValue,
    images: [...props.modelValue.images, ...newFiles]
  })
}

const removeImage = (index: number) => {
  const image = props.modelValue.images?.[index]
  if (!image) return

  if (image.id) {
    props.onScheduleImageForDeletion(image.id)
  }
  const updatedImages = [...props.modelValue.images]
  updatedImages.splice(index, 1)
  emit('update:modelValue', { ...props.modelValue, images: updatedImages })
}
</script>