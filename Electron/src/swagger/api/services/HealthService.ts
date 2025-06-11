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
     * This endpoint can be used to verify that the server is running and responding to requests.
     * It checks both database connectivity and song service availability.
     *
     * Returns:
     * Response: HTTP 200 OK if all services are healthy,
     * HTTP 500 if services are unhealthy but reachable,
     * HTTP 503 if specific service errors occur.
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
