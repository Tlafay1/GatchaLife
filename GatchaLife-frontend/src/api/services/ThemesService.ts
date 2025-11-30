/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
 
import type { Theme } from '../models/Theme';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ThemesService {
    /**
     * @param id
     * @param name
     * @param category
     * @param ambiance
     * @param search A search term.
     * @returns Theme
     * @throws ApiError
     */
    public static themesList(
        id?: string,
        name?: string,
        category?: string,
        ambiance?: string,
        search?: string,
    ): CancelablePromise<Array<Theme>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/themes/',
            query: {
                'id': id,
                'name': name,
                'category': category,
                'ambiance': ambiance,
                'search': search,
            },
        });
    }
    /**
     * @param data
     * @returns Theme
     * @throws ApiError
     */
    public static themesCreate(
        data: Theme,
    ): CancelablePromise<Theme> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/themes/',
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this theme.
     * @returns Theme
     * @throws ApiError
     */
    public static themesRead(
        id: number,
    ): CancelablePromise<Theme> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/themes/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @param id A unique integer value identifying this theme.
     * @param data
     * @returns Theme
     * @throws ApiError
     */
    public static themesUpdate(
        id: number,
        data: Theme,
    ): CancelablePromise<Theme> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/themes/{id}/',
            path: {
                'id': id,
            },
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this theme.
     * @param data
     * @returns Theme
     * @throws ApiError
     */
    public static themesPartialUpdate(
        id: number,
        data: Theme,
    ): CancelablePromise<Theme> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/themes/{id}/',
            path: {
                'id': id,
            },
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this theme.
     * @returns void
     * @throws ApiError
     */
    public static themesDelete(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/themes/{id}/',
            path: {
                'id': id,
            },
        });
    }
}
