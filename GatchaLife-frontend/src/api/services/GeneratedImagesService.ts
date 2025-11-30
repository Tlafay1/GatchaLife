/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
 
import type { GeneratedImage } from '../models/GeneratedImage';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class GeneratedImagesService {
    /**
     * @param id
     * @param search A search term.
     * @returns GeneratedImage
     * @throws ApiError
     */
    public static generatedImagesList(
        id?: string,
        search?: string,
    ): CancelablePromise<Array<GeneratedImage>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/generated-images/',
            query: {
                'id': id,
                'search': search,
            },
        });
    }
    /**
     * @param data
     * @returns GeneratedImage
     * @throws ApiError
     */
    public static generatedImagesCreate(
        data: GeneratedImage,
    ): CancelablePromise<GeneratedImage> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/generated-images/',
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this generated image.
     * @returns GeneratedImage
     * @throws ApiError
     */
    public static generatedImagesRead(
        id: number,
    ): CancelablePromise<GeneratedImage> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/generated-images/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @param id A unique integer value identifying this generated image.
     * @param data
     * @returns GeneratedImage
     * @throws ApiError
     */
    public static generatedImagesUpdate(
        id: number,
        data: GeneratedImage,
    ): CancelablePromise<GeneratedImage> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/generated-images/{id}/',
            path: {
                'id': id,
            },
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this generated image.
     * @param data
     * @returns GeneratedImage
     * @throws ApiError
     */
    public static generatedImagesPartialUpdate(
        id: number,
        data: GeneratedImage,
    ): CancelablePromise<GeneratedImage> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/generated-images/{id}/',
            path: {
                'id': id,
            },
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this generated image.
     * @returns void
     * @throws ApiError
     */
    public static generatedImagesDelete(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/generated-images/{id}/',
            path: {
                'id': id,
            },
        });
    }
}
