/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class PlaylistsService {
    /**
     * Get Playlist
     * Get playlsit
     *
     * Args:
     * name (str): playlist name
     * @param name
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getPlaylistPlaylistsNameGet(
        name: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/playlists/{name}',
            path: {
                'name': name,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Playlist
     * Update playlist
     *
     * Args:
     * photo (str): playlist new photo
     * description (str): playlist new description
     * song_names (list[str], optional): playlist new song names. Defaults to Body(...).
     * new_name (str | None, optional): playlist new name. Defaults to None.
     * @param name
     * @param photo
     * @param description
     * @param requestBody
     * @param newName
     * @returns any Successful Response
     * @throws ApiError
     */
    public static updatePlaylistPlaylistsNamePut(
        name: string,
        photo: string,
        description: string,
        requestBody: Array<string>,
        newName?: (string | null),
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/playlists/{name}',
            path: {
                'name': name,
            },
            query: {
                'photo': photo,
                'description': description,
                'new_name': newName,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Playlist
     * Delete playlsit
     *
     * Args:
     * name (str): playlist name
     * @param name
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deletePlaylistPlaylistsNameDelete(
        name: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/playlists/{name}',
            path: {
                'name': name,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Create Playlist
     * Create playlist
     *
     * Args:
     * name (str): playlist name
     * photo (str): playlist photo
     * description (str): playlist description
     * song_names (list[str]): list of song names included in playlist.
     * @param name
     * @param photo
     * @param description
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createPlaylistPlaylistsPost(
        name: string,
        photo: string,
        description: string,
        requestBody: Array<string>,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/playlists/',
            query: {
                'name': name,
                'photo': photo,
                'description': description,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Playlists
     * Return all playlists
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getPlaylistsPlaylistsGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/playlists/',
        });
    }
    /**
     * Get Selected Playlists
     * Get selected playlists
     *
     * Args:
     * names (str): playlist names
     * @param names
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getSelectedPlaylistsPlaylistsSelectedNamesGet(
        names: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/playlists/selected/{names}',
            path: {
                'names': names,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
