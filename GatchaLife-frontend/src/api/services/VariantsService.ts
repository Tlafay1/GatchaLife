/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CharacterVariant } from '../models/CharacterVariant';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class VariantsService {
    /**
     * @param character
     * @returns CharacterVariant
     * @throws ApiError
     */
    public static variantsList(
        character?: string,
    ): CancelablePromise<Array<CharacterVariant>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/variants/',
            query: {
                'character': character,
            },
        });
    }
    /**
     * @param data
     * @returns CharacterVariant
     * @throws ApiError
     */
    public static variantsCreate(
        data: CharacterVariant,
    ): CancelablePromise<CharacterVariant> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/variants/',
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this character variant.
     * @returns CharacterVariant
     * @throws ApiError
     */
    public static variantsRead(
        id: number,
    ): CancelablePromise<CharacterVariant> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/variants/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @param id A unique integer value identifying this character variant.
     * @param data
     * @returns CharacterVariant
     * @throws ApiError
     */
    public static variantsUpdate(
        id: number,
        data: CharacterVariant,
    ): CancelablePromise<CharacterVariant> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/variants/{id}/',
            path: {
                'id': id,
            },
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this character variant.
     * @param data
     * @returns CharacterVariant
     * @throws ApiError
     */
    public static variantsPartialUpdate(
        id: number,
        data: CharacterVariant,
    ): CancelablePromise<CharacterVariant> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/variants/{id}/',
            path: {
                'id': id,
            },
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this character variant.
     * @returns void
     * @throws ApiError
     */
    public static variantsDelete(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/variants/{id}/',
            path: {
                'id': id,
            },
        });
    }
}
