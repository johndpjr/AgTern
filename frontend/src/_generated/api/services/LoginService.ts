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
            url: '/login/token',
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
            url: '/login/users/me',
        });
    }

    /**
     * Register User
     * Registers a user
     * @param username
     * @param fullName
     * @param email
     * @param password
     * @returns any Successful Response
     * @throws ApiError
     */
    public static registerUser(
        username: string,
        fullName: string,
        email: string,
        password: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/login/users/register',
            query: {
                'username': username,
                'full_name': fullName,
                'email': email,
                'password': password,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete User
     * Deletes a user. Requires password confirmation
     * @param username
     * @param password
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteUser(
        username: string,
        password: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/loginusers/delete',
            query: {
                'username': username,
                'password': password,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Users
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getUsers(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/login/get_users',
        });
    }

    /**
     * Update Columns
     * Updates the user model
     * @returns any Successful Response
     * @throws ApiError
     */
    public static updateColumns(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/login/update_columns',
        });
    }

    /**
     * Init Database
     * Initializes the user model in the database
     * @returns any Successful Response
     * @throws ApiError
     */
    public static initDatabase(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/login/init_user_db',
        });
    }

}
