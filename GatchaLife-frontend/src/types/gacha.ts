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
  unlock_level: number;
  // New fields
  wiki_source_text?: string;
  identity_face_image?: File | null; // For upload
  identity_face_image_url?: string | null; // For display
  body_type_description?: string;
  height_perception?: 'SHORT' | 'AVERAGE' | 'TALL' | 'GIANT' | '';
  hair_prompt?: string;
  eye_prompt?: string;
  visual_traits?: string[]; // Simplified as array of strings
  lore_tags?: string[];
  affinity_environments?: { name: string; visual_prompt: string }[];
  clashing_environments?: string[];
  negative_traits_suggestion?: string;
}