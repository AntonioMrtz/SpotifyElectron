/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_create_song_songs__post } from '../models/Body_create_song_songs__post';
import type { Genre } from '../models/Genre';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class SongsService {
    /**
     * Get Song
     * Get song
     *
     * Args:
     * name: song name
     * token: JWT info
     * @param name
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getSongSongsNameGet(
        name: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/songs/{name}',
            path: {
                'name': name,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Song
     * Delete song
     *
     * Args:
     * name: song name
     * @param name
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteSongSongsNameDelete(
        name: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/songs/{name}',
            path: {
                'name': name,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Create Song
     * Create song
     *
     * Args:
     * name: song name
     * genre: genre
     * photo: photo
     * file: song file
     * token: JWT info
     * @param name
     * @param genre
     * @param photo
     * @param formData
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createSongSongsPost(
        name: string,
        genre: Genre,
        photo: string,
        formData: Body_create_song_songs__post,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/songs/',
            query: {
                'name': name,
                'genre': genre,
                'photo': photo,
            },
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Song Metadata
     * Get song metadata
     *
     * Args:
     * name: the song name
     * token: JWT info
     * @param name
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getSongMetadataSongsMetadataNameGet(
        name: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/songs/metadata/{name}',
            path: {
                'name': name,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Increase Song Streams
     * Increase total streams of a song
     *
     * Args:
     * name: song name
     * token: JWT info
     * @param name
     * @returns any Successful Response
     * @throws ApiError
     */
    public static increaseSongStreamsSongsNameStreamsPatch(
        name: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/songs/{name}/streams',
            path: {
                'name': name,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Songs By Genre
     * Get songs by genre
     *
     * Args:
     * genre: the genre to match
     * token: JWT info
     * @param genre
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getSongsByGenreSongsGenresGenreGet(
        genre: Genre,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/songs/genres/{genre}',
            path: {
                'genre': genre,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
