/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Style } from '../models/Style';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class StylesService {
    /**
     * @param id
     * @param name
     * @param rarityId
     * @param rarityName
     * @param search A search term.
     * @returns Style
     * @throws ApiError
     */
    public static stylesList(
        id?: string,
        name?: string,
        rarityId?: string,
        rarityName?: string,
        search?: string,
    ): CancelablePromise<Array<Style>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/styles/',
            query: {
                'id': id,
                'name': name,
                'rarity__id': rarityId,
                'rarity__name': rarityName,
                'search': search,
            },
        });
    }
    /**
     * @param data
     * @returns Style
     * @throws ApiError
     */
    public static stylesCreate(
        data: Style,
    ): CancelablePromise<Style> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/styles/',
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this style.
     * @returns Style
     * @throws ApiError
     */
    public static stylesRead(
        id: number,
    ): CancelablePromise<Style> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/styles/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @param id A unique integer value identifying this style.
     * @param data
     * @returns Style
     * @throws ApiError
     */
    public static stylesUpdate(
        id: number,
        data: Style,
    ): CancelablePromise<Style> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/styles/{id}/',
            path: {
                'id': id,
            },
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this style.
     * @param data
     * @returns Style
     * @throws ApiError
     */
    public static stylesPartialUpdate(
        id: number,
        data: Style,
    ): CancelablePromise<Style> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/styles/{id}/',
            path: {
                'id': id,
            },
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this style.
     * @returns void
     * @throws ApiError
     */
    public static stylesDelete(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/styles/{id}/',
            path: {
                'id': id,
            },
        });
    }
}
