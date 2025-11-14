/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Series } from '../models/Series';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class SeriesService {
    /**
     * @returns Series
     * @throws ApiError
     */
    public static seriesList(): CancelablePromise<Array<Series>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/series/',
        });
    }
    /**
     * @param data
     * @returns Series
     * @throws ApiError
     */
    public static seriesCreate(
        data: Series,
    ): CancelablePromise<Series> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/series/',
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this series.
     * @returns Series
     * @throws ApiError
     */
    public static seriesRead(
        id: number,
    ): CancelablePromise<Series> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/series/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @param id A unique integer value identifying this series.
     * @param data
     * @returns Series
     * @throws ApiError
     */
    public static seriesUpdate(
        id: number,
        data: Series,
    ): CancelablePromise<Series> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/series/{id}/',
            path: {
                'id': id,
            },
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this series.
     * @param data
     * @returns Series
     * @throws ApiError
     */
    public static seriesPartialUpdate(
        id: number,
        data: Series,
    ): CancelablePromise<Series> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/series/{id}/',
            path: {
                'id': id,
            },
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this series.
     * @returns void
     * @throws ApiError
     */
    public static seriesDelete(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/series/{id}/',
            path: {
                'id': id,
            },
        });
    }
}
