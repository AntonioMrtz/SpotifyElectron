/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class StreamService {
    /**
     * Stream Song
     * Streams song audio
     *
     * Args:
     * name: song name
     * request: incoming request
     * token: JWT info
     * @param name
     * @returns any Successful Response
     * @throws ApiError
     */
    public static streamSongStreamNameGet(
        name: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/stream/{name}',
            path: {
                'name': name,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
