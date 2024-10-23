/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class UsersService {
  /**
   * Get Who Am I
   * Returns token info from JWT
   *
   * Args:
   * token (TokenData): the jwt token. Defaults to None.
   * @returns any Successful Response
   * @throws ApiError
   */
  public static getWhoAmIUsersWhoamiGet(): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: 'GET',
      url: '/users/whoami',
    });
  }
  /**
   * Get User
   * Get user by name
   *
   * Args:
   * name (str): user name
   * @param name
   * @returns any Successful Response
   * @throws ApiError
   */
  public static getUserUsersNameGet(name: string): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: 'GET',
      url: '/users/{name}',
      path: {
        name: name,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Delete User
   * Delete user
   *
   * Args:
   * name (str): user name
   * @param name
   * @returns any Successful Response
   * @throws ApiError
   */
  public static deleteUserUsersNameDelete(
    name: string,
  ): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: 'DELETE',
      url: '/users/{name}',
      path: {
        name: name,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Create User
   * Create user
   *
   * Args:
   * name (str): user name
   * photo (str): user photo
   * password (str): user password
   * @param name
   * @param photo
   * @param password
   * @returns any Successful Response
   * @throws ApiError
   */
  public static createUserUsersPost(
    name: string,
    photo: string,
    password: string,
  ): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: 'POST',
      url: '/users/',
      query: {
        name: name,
        photo: photo,
        password: password,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Patch Playback History
   * Add song to playback history
   *
   * Args:
   * name (str): user name
   * song_name (str): song name
   * @param name
   * @param songName
   * @returns any Successful Response
   * @throws ApiError
   */
  public static patchPlaybackHistoryUsersNamePlaybackHistoryPatch(
    name: string,
    songName: string,
  ): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: 'PATCH',
      url: '/users/{name}/playback_history',
      path: {
        name: name,
      },
      query: {
        song_name: songName,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Get User Playback History
   * Get user song playback history
   *
   * Args:
   * name (str): user name
   * @param name
   * @returns any Successful Response
   * @throws ApiError
   */
  public static getUserPlaybackHistoryUsersNamePlaybackHistoryGet(
    name: string,
  ): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: 'GET',
      url: '/users/{name}/playback_history',
      path: {
        name: name,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Patch Saved Playlists
   * Add playlist to saved list
   *
   * Args:
   * name (str): user name
   * playlist_name (str): saved playlist
   * @param name
   * @param playlistName
   * @returns any Successful Response
   * @throws ApiError
   */
  public static patchSavedPlaylistsUsersNameSavedPlaylistsPatch(
    name: string,
    playlistName: string,
  ): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: 'PATCH',
      url: '/users/{name}/saved_playlists',
      path: {
        name: name,
      },
      query: {
        playlist_name: playlistName,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Delete Saved Playlists
   * Delete playlist from saved list of user
   *
   * Args:
   * name (str): user name
   * playlist_name (str): playlist name
   * @param name
   * @param playlistName
   * @returns any Successful Response
   * @throws ApiError
   */
  public static deleteSavedPlaylistsUsersNameSavedPlaylistsDelete(
    name: string,
    playlistName: string,
  ): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: 'DELETE',
      url: '/users/{name}/saved_playlists',
      path: {
        name: name,
      },
      query: {
        playlist_name: playlistName,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Get User Relevant Playlists
   * Get relevant playlists for user
   *
   * Args:
   * name (str): user name
   * @param name
   * @returns any Successful Response
   * @throws ApiError
   */
  public static getUserRelevantPlaylistsUsersNameRelevantPlaylistsGet(
    name: string,
  ): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: 'GET',
      url: '/users/{name}/relevant_playlists',
      path: {
        name: name,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Get User Playlists
   * Get playlists created by the user
   *
   * Args:
   * name (str): user name
   * @param name
   * @returns any Successful Response
   * @throws ApiError
   */
  public static getUserPlaylistsUsersNamePlaylistsGet(
    name: string,
  ): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: 'GET',
      url: '/users/{name}/playlists',
      path: {
        name: name,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Get User Playlists Names
   * Get playlist names created by user
   *
   * Args:
   * name (str): user name
   * @param name
   * @returns any Successful Response
   * @throws ApiError
   */
  public static getUserPlaylistsNamesUsersNamePlaylistNamesGet(
    name: string,
  ): CancelablePromise<any> {
    return __request(OpenAPI, {
      method: 'GET',
      url: '/users/{name}/playlist_names',
      path: {
        name: name,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
