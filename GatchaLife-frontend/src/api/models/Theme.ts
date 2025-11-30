/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type Theme = {
    readonly id?: number;
    name: string;
    /**
     * Ex: Technologie, Fitness, Fantaisie
     */
    category?: string;
    ambiance?: string;
    /**
     * Prompts pour l'IA (ex: moniteurs multiples, lignes de code)
     */
    keywords_theme?: string;
    /**
     * Le prompt de fond complet pour l'IA
     */
    prompt_background?: string;
    /**
     * Rappel sur comment intégrer le personnage
     */
    integration_idea?: string;
};

