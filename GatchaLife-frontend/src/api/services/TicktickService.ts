/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class TicktickService {
    /**
     * Returns full history of processed tasks with all reward details.
     * @returns any
     * @throws ApiError
     */
    public static ticktickHistory(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/ticktick/history/',
        });
    }
    /**
     * Returns daily aggregated XP and Coin stats for the last 30 days.
     * @returns any
     * @throws ApiError
     */
    public static ticktickProgression(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/ticktick/progression/',
        });
    }
    /**
     * @returns any
     * @throws ApiError
     */
    public static ticktickStats(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/ticktick/stats/',
        });
    }
    /**
     * Webhook endpoint for Zapier to call when a task is completed.
     * Expected payload from Zapier:
     * {
         * "id": "string",
         * "task_name": "string",
         * "list": "string" (optional),
         * "tag": "List[string]" (optional),
         * "priority": "string" (optional),
         * "timestamp": number (optional),
         * "link_to_task": "string" (optional),
         * "repeat_flag": "string" (optional)
         * }
         * @returns any
         * @throws ApiError
         */
        public static ticktickWebhookCreate(): CancelablePromise<any> {
            return __request(OpenAPI, {
                method: 'POST',
                url: '/ticktick/webhook/',
            });
        }
    }
