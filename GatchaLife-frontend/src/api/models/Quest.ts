/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type Quest = {
    readonly id?: number;
    title: string;
    description?: string;
    xp_reward?: number;
    currency_reward?: number;
    type?: Quest.type;
    /**
     * Key to identify the condition in code (e.g., 'task_completed')
     */
    condition_key: string;
};
export namespace Quest {
    export enum type {
        DAILY = 'DAILY',
        ACHIEVEMENT = 'ACHIEVEMENT',
    }
}

