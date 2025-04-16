/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class SearchService {
    /**
     * Get Search Name
     * Search for items that partially match name
     *
     * Args:
     * ----
     * name: name to match
     * token: JWT info
     * @param name
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getSearchNameSearchGet(
        name: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/search/',
            query: {
                'name': name,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
