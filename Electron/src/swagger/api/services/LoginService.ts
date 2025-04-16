/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_login_user_login__post } from '../models/Body_login_user_login__post';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class LoginService {
    /**
     * Login User
     * Login user
     *
     * Args:
     * ----
     * form_data: user and password
     * @param formData
     * @returns any Successful Response
     * @throws ApiError
     */
    public static loginUserLoginPost(
        formData: Body_login_user_login__post,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/login/',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Login User With Jwt
     * Login user with token
     *
     * Args:
     * token: the user token
     * @param token
     * @returns any Successful Response
     * @throws ApiError
     */
    public static loginUserWithJwtLoginTokenTokenPost(
        token: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/login/token/{token}',
            path: {
                'token': token,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
