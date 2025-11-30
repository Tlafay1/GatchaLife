<template>
    <div class="max-w-4xl mx-auto p-6">
        <div class="flex items-center justify-between mb-6">
            <h1 class="text-3xl font-bold">Styles</h1>
            <Button @click="openCreateDialog">
                <Plus class="w-4 h-4 mr-2" /> New Style
            </Button>
        </div>

        <div v-if="isLoading" class="text-center text-muted-foreground">Loading styles...</div>

        <div v-else-if="styles?.length === 0" class="text-center py-12 border-2 border-dashed rounded-lg">
            <p class="text-muted-foreground mb-2">No styles found.</p>
            <Button variant="link" @click="openCreateDialog">Create your first style</Button>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card v-for="style in styles" :key="style.id">
                <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle class="text-lg font-bold">{{ style.name }}</CardTitle>
                    <div class="flex gap-2">
                        <Button variant="ghost" size="icon" @click="openEditDialog(style)">
                            <Pencil class="w-4 h-4" />
                        </Button>
                        <Button variant="ghost" size="icon" class="text-destructive hover:text-destructive"
                            @click="handleDelete(style.id!)">
                            <Trash2 class="w-4 h-4" />
                        </Button>
                    </div>
                </CardHeader>
                <CardContent>
                    <div class="space-y-2 text-sm">
                        <div class="flex justify-between">
                            <span class="text-muted-foreground">Rarity:</span>
                            <span class="font-medium">{{ getRarityName(style.rarity) }}</span>
                        </div>
                        <div>
                            <span class="text-muted-foreground block mb-1">Keywords:</span>
                            <div class="bg-muted p-2 rounded text-xs font-mono break-all">{{ style.style_keywords }}
                            </div>
                        </div>
                        <div v-if="style.composition_hint">
                            <span class="text-muted-foreground block mb-1">Composition Hint:</span>
                            <div class="bg-muted p-2 rounded text-xs font-mono break-all text-blue-400/80">{{
                                style.composition_hint }}</div>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>

        <!-- Create/Edit Dialog -->
        <Dialog v-model:open="isDialogOpen">
            <DialogContent class="sm:max-w-[500px]">
                <DialogHeader>
                    <DialogTitle>{{ isEditing ? 'Edit Style' : 'Create New Style' }}</DialogTitle>
                    <DialogDescription>
                        Define the visual style and prompt modifiers.
                    </DialogDescription>
                </DialogHeader>

                <div class="grid gap-4 py-4">
                    <div class="grid gap-2">
                        <Label>Name</Label>
                        <Input v-model="form.name" placeholder="e.g. Anime, Realistic, Chibi" />
                    </div>

                    <div class="grid gap-2">
                        <Label>Rarity</Label>
                        <Select v-model="form.rarity">
                            <SelectTrigger>
                                <SelectValue placeholder="Select rarity" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem v-for="r in rarities" :key="r.id" :value="String(r.id)">
                                    {{ r.name }}
                                </SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    <div class="grid gap-2">
                        <Label>Unlock Level</Label>
                        <Input v-model="form.unlock_level" type="number" min="1" placeholder="1" />
                        <p class="text-xs text-muted-foreground">Player level required to unlock this style.</p>
                    </div>

                    <div class="grid gap-2">
                        <Label>Style Keywords</Label>
                        <Textarea v-model="form.style_keywords"
                            placeholder="e.g. anime style, cel shaded, vibrant colors" class="h-24" />
                        <p class="text-xs text-muted-foreground">Added to the prompt during generation.</p>
                    </div>

                    <div class="grid gap-2">
                        <Label>Composition Hint</Label>
                        <Textarea v-model="form.composition_hint" placeholder="e.g. full body shot, dynamic pose" />
                    </div>
                </div>

                <DialogFooter>
                    <Button @click="handleSubmit" :disabled="isSubmitting">
                        {{ isSubmitting ? 'Saving...' : 'Save Style' }}
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
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useStylesList, useCreateStyle, useUpdateStyle, useDeleteStyle, useRaritiesList } from '@/lib/api-client'
import type { Style } from '@/api'

const { data: styles, isLoading } = useStylesList()
const { data: rarities } = useRaritiesList()

const { mutateAsync: createStyle, isPending: isCreating } = useCreateStyle()
const { mutateAsync: updateStyle, isPending: isUpdating } = useUpdateStyle()
const { mutate: deleteStyle } = useDeleteStyle()

const isDialogOpen = ref(false)
const editingId = ref<number | null>(null)
const isEditing = computed(() => !!editingId.value)
const isSubmitting = computed(() => isCreating.value || isUpdating.value)

const form = reactive({
    name: '',
    style_keywords: '',
    composition_hint: '',
    rarity: '',
    unlock_level: 1
})

const getRarityName = (id: number) => {
    return rarities.value?.find(r => r.id === id)?.name || `ID: ${id}`
}

const openCreateDialog = () => {
    editingId.value = null
    form.name = ''
    form.style_keywords = ''
    form.composition_hint = ''
    form.rarity = ''
    form.unlock_level = 1
    isDialogOpen.value = true
}

const openEditDialog = (style: Style) => {
    editingId.value = style.id!
    form.name = style.name
    form.style_keywords = style.style_keywords || ''
    form.composition_hint = style.composition_hint || ''
    form.rarity = String(style.rarity)
    form.unlock_level = style.unlock_level || 1
    isDialogOpen.value = true
}

const handleSubmit = async () => {
    if (!form.name || !form.rarity || !form.style_keywords) {
        alert('Please fill in all required fields')
        return
    }

    try {
        const payload = {
            name: form.name,
            style_keywords: form.style_keywords,
            composition_hint: form.composition_hint,
            rarity: parseInt(form.rarity),
            unlock_level: form.unlock_level
        }

    if (isEditing.value && editingId.value) {
      await updateStyle({ id: editingId.value, ...payload })
    } else {
      await createStyle(payload)
    }
    isDialogOpen.value = false
  } catch (error) {
    console.error(error)
    alert('Failed to save style')
  }
}

const handleDelete = (id: number) => {
  if (confirm('Are you sure you want to delete this style?')) {
    deleteStyle(id)
  }
}
</script>
