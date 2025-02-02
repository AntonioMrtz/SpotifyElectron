/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ArtistsService {
    /**
     * Get Artist
     * Get artist by name
     *
     * Args:
     * name (str): artist name
     * token (Annotated[TokenData, Depends): JWT info
     * @param name
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getArtistArtistsNameGet(
        name: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/artists/{name}',
            path: {
                'name': name,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Create Artist
     * Create artist
     *
     * Args:
     * name (str): artist name
     * photo (str): artist photo
     * password (str): artist password
     * @param name
     * @param photo
     * @param password
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createArtistArtistsPost(
        name: string,
        photo: string,
        password: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/artists/',
            query: {
                'name': name,
                'photo': photo,
                'password': password,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Artists
     * Get all artists
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getArtistsArtistsGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/artists/',
        });
    }
    /**
     * Get Artist Songs
     * Get artist songs
     * @param name
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getArtistSongsArtistsNameSongsGet(
        name: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/artists/{name}/songs',
            path: {
                'name': name,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
