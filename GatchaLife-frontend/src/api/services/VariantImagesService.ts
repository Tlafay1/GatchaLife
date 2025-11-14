/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { VariantReferenceImage } from '../models/VariantReferenceImage';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class VariantImagesService {
    /**
     * @param variant
     * @returns VariantReferenceImage
     * @throws ApiError
     */
    public static variantImagesList(
        variant?: string,
    ): CancelablePromise<Array<VariantReferenceImage>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/variant-images/',
            query: {
                'variant': variant,
            },
        });
    }
    /**
     * @param data
     * @returns VariantReferenceImage
     * @throws ApiError
     */
    public static variantImagesCreate(
        data: VariantReferenceImage,
    ): CancelablePromise<VariantReferenceImage> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/variant-images/',
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this variant reference image.
     * @returns VariantReferenceImage
     * @throws ApiError
     */
    public static variantImagesRead(
        id: number,
    ): CancelablePromise<VariantReferenceImage> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/variant-images/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @param id A unique integer value identifying this variant reference image.
     * @param data
     * @returns VariantReferenceImage
     * @throws ApiError
     */
    public static variantImagesUpdate(
        id: number,
        data: VariantReferenceImage,
    ): CancelablePromise<VariantReferenceImage> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/variant-images/{id}/',
            path: {
                'id': id,
            },
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this variant reference image.
     * @param data
     * @returns VariantReferenceImage
     * @throws ApiError
     */
    public static variantImagesPartialUpdate(
        id: number,
        data: VariantReferenceImage,
    ): CancelablePromise<VariantReferenceImage> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/variant-images/{id}/',
            path: {
                'id': id,
            },
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this variant reference image.
     * @returns void
     * @throws ApiError
     */
    public static variantImagesDelete(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/variant-images/{id}/',
            path: {
                'id': id,
            },
        });
    }
}
