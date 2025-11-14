import type { Series, Character, CharacterVariant } from '@/api';

// Re-export API types for use in components
export type { Series, Character, CharacterVariant };

// --- Frontend Specific State Types ---

// Even if the model removed 'view_type', the UI template still uses it.
// We keep it in the local state to satisfy the UI.
export type ViewType = 'front' | 'side' | 'action' | 'detail';

export interface LocalVariantImage {
  file?: File;       // New file to upload
  url?: string;      // Preview URL
  view_type: ViewType;
  is_new?: boolean;
}

export interface LocalVariantForm {
  name: string;
  visual_description: string; // Maps to 'description' in backend
  images: LocalVariantImage[];
}

export interface CharacterFormState {
  name: string;
  series: string; // String to handle Select value binding
  base_description: string;
  variants: LocalVariantForm[];
}