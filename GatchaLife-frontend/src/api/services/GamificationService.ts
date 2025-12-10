/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Player } from '../models/Player';
import type { PlayerQuest } from '../models/PlayerQuest';
import type { UserCard } from '../models/UserCard';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class GamificationService {
    /**
     * @returns UserCard
     * @throws ApiError
     */
    public static gamificationCollectionList(): CancelablePromise<Array<UserCard>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/gamification/collection/',
        });
    }
    /**
     * @param id
     * @returns UserCard
     * @throws ApiError
     */
    public static gamificationCollectionRead(
        id: string,
    ): CancelablePromise<UserCard> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/gamification/collection/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @param id
     * @param data
     * @returns UserCard
     * @throws ApiError
     */
    public static gamificationCollectionRerollImage(
        id: string,
        data: UserCard,
    ): CancelablePromise<UserCard> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/gamification/collection/{id}/reroll_image/',
            path: {
                'id': id,
            },
            body: data,
        });
    }
    /**
     * @returns any
     * @throws ApiError
     */
    public static gamificationGatchaRoll(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/gamification/gatcha/roll/',
        });
    }
    /**
     * @returns Player
     * @throws ApiError
     */
    public static gamificationPlayerList(): CancelablePromise<Array<Player>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/gamification/player/',
        });
    }
    /**
     * @param data
     * @returns Player
     * @throws ApiError
     */
    public static gamificationPlayerCreate(
        data: Player,
    ): CancelablePromise<Player> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/gamification/player/',
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this player.
     * @returns Player
     * @throws ApiError
     */
    public static gamificationPlayerRead(
        id: number,
    ): CancelablePromise<Player> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/gamification/player/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @param id A unique integer value identifying this player.
     * @param data
     * @returns Player
     * @throws ApiError
     */
    public static gamificationPlayerUpdate(
        id: number,
        data: Player,
    ): CancelablePromise<Player> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/gamification/player/{id}/',
            path: {
                'id': id,
            },
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this player.
     * @param data
     * @returns Player
     * @throws ApiError
     */
    public static gamificationPlayerPartialUpdate(
        id: number,
        data: Player,
    ): CancelablePromise<Player> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/gamification/player/{id}/',
            path: {
                'id': id,
            },
            body: data,
        });
    }
    /**
     * @param id A unique integer value identifying this player.
     * @returns void
     * @throws ApiError
     */
    public static gamificationPlayerDelete(
        id: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/gamification/player/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @returns PlayerQuest
     * @throws ApiError
     */
    public static gamificationQuestsList(): CancelablePromise<Array<PlayerQuest>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/gamification/quests/',
        });
    }
    /**
     * @param id
     * @returns PlayerQuest
     * @throws ApiError
     */
    public static gamificationQuestsRead(
        id: string,
    ): CancelablePromise<PlayerQuest> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/gamification/quests/{id}/',
            path: {
                'id': id,
            },
        });
    }
    /**
     * @param id
     * @param data
     * @returns PlayerQuest
     * @throws ApiError
     */
    public static gamificationQuestsClaim(
        id: string,
        data: PlayerQuest,
    ): CancelablePromise<PlayerQuest> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/gamification/quests/{id}/claim/',
            path: {
                'id': id,
            },
            body: data,
        });
    }
}
