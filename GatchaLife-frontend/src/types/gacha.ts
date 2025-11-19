import type { Series, Character, CharacterVariant } from '@/api';

// Re-export API types for use in components
export type { Series, Character, CharacterVariant };

export interface LocalVariantImage {
  id?: number;       // Existing image ID
  file?: File;       // New file to upload
  url?: string;      // Preview URL for existing or new
  is_new?: boolean;  // Flag for new uploads
}

export interface LocalVariantForm {
  id?: number;       // Existing variant ID
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