/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CharacterVariant } from './CharacterVariant';
import type { VariantReferenceImage } from './VariantReferenceImage';
export type Character = {
    readonly id?: number;
    name: string;
    description?: string;
    readonly images?: Array<VariantReferenceImage>;
    readonly variants?: Array<CharacterVariant>;
    series: number;
    unlock_level?: number;
    readonly identity_face_image?: string | null;
    /**
     * ex: petite stature, slender build, flat chest
     */
    body_type_description?: string;
    /**
     * ex: short, tall, giant
     */
    height_perception?: Character.height_perception;
    /**
     * Description visuelle des cheveux
     */
    hair_prompt?: string;
    /**
     * Description visuelle des yeux
     */
    eye_prompt?: string;
    /**
     * Liste de traits physiques immuables ex: ['scar on left eye', 'pale skin']
     */
    visual_traits?: any;
    /**
     * ex: ['stealth', 'modern', 'cynical']
     */
    lore_tags?: any;
    /**
     * ex: [{'name': 'shadows', 'visual_prompt': 'dark alley'}]
     */
    affinity_environments?: any;
    /**
     * ex: ['holy church', 'bright beach']
     */
    clashing_environments?: any;
    /**
     * Negative prompt morphologique
     */
    negative_traits_suggestion?: string;
};
export namespace Character {
    /**
     * ex: short, tall, giant
     */
    export enum height_perception {
        SHORT = 'SHORT',
        AVERAGE = 'AVERAGE',
        TALL = 'TALL',
        GIANT = 'GIANT',
    }
}

