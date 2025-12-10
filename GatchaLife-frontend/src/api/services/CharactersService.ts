/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Character } from '../models/Character';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class CharactersService {
    /**
     * @param series
     * @param search A search term.
     * @returns Character
     * @throws ApiError
     */
    public static charactersList(
        series?: string,
        search?: string,
    ): CancelablePromise<Array<Character>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/characters/',
            query: {
                'series': series,
                'search': search,
            },
        });
    }
    /**
     * @param data
     * @returns Character
     * @throws ApiError
     */
    public static charactersCreate(
        data: Character,
    ): CancelablePromise<Character> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/characters/',
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this character.
     * @returns Character
     * @throws ApiError
     */
    public static charactersRead(
        id: number,
    ): CancelablePromise<Character> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/characters/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @param id A unique integer value identifying this character.
     * @param data
     * @returns Character
     * @throws ApiError
     */
    public static charactersUpdate(
        id: number,
        data: Character,
    ): CancelablePromise<Character> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/characters/{id}/',
            path: {
                'id': id,
            },
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this character.
     * @param data
     * @returns Character
     * @throws ApiError
     */
    public static charactersPartialUpdate(
        id: number,
        data: Character,
    ): CancelablePromise<Character> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/characters/{id}/',
            path: {
                'id': id,
            },
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this character.
     * @returns void
     * @throws ApiError
     */
    public static charactersDelete(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/characters/{id}/',
            path: {
                'id': id,
            },
        });
    }
}
