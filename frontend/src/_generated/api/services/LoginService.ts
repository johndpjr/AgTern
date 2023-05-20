/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_login } from '../models/Body_login';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class LoginService {

    /**
     * Login
     * @param formData
     * @returns any Successful Response
     * @throws ApiError
     */
    public static login(
        formData: Body_login,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/login/token',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Users Me
     * @returns any Successful Response
     * @throws ApiError
     */
    public static readUsersMe(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/login/users/me',
        });
    }

}
