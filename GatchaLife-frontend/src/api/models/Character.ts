/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
 
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
};

