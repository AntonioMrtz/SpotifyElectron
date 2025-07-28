/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class HealthService {
    /**
     * Health Check Endpoint
     * Validates if the application has launched correctly by returning a health check response
     *
     * Response:
     * HTTP 200 OK with "OK" content if all services are healthy.
     * HTTP 503 Service Unavailable with specific error message if a particular
     * service health check fails
     * HTTP 500 Internal Server Error with generic error message for unexpected errors
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getHealthHealthGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/health/',
        });
    }
}
