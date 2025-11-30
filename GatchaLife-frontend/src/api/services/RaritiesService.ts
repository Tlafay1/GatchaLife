/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
 
import type { Rarity } from '../models/Rarity';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class RaritiesService {
    /**
     * @param id
     * @param name
     * @param search A search term.
     * @returns Rarity
     * @throws ApiError
     */
    public static raritiesList(
        id?: string,
        name?: string,
        search?: string,
    ): CancelablePromise<Array<Rarity>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/rarities/',
            query: {
                'id': id,
                'name': name,
                'search': search,
            },
        });
    }
    /**
     * @param data
     * @returns Rarity
     * @throws ApiError
     */
    public static raritiesCreate(
        data: Rarity,
    ): CancelablePromise<Rarity> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/rarities/',
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this rarity.
     * @returns Rarity
     * @throws ApiError
     */
    public static raritiesRead(
        id: number,
    ): CancelablePromise<Rarity> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/rarities/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @param id A unique integer value identifying this rarity.
     * @param data
     * @returns Rarity
     * @throws ApiError
     */
    public static raritiesUpdate(
        id: number,
        data: Rarity,
    ): CancelablePromise<Rarity> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/rarities/{id}/',
            path: {
                'id': id,
            },
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this rarity.
     * @param data
     * @returns Rarity
     * @throws ApiError
     */
    public static raritiesPartialUpdate(
        id: number,
        data: Rarity,
    ): CancelablePromise<Rarity> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/rarities/{id}/',
            path: {
                'id': id,
            },
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this rarity.
     * @returns void
     * @throws ApiError
     */
    public static raritiesDelete(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/rarities/{id}/',
            path: {
                'id': id,
            },
        });
    }
}
