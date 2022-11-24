/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Internship } from '../models/Internship';
import type { InternshipCreate } from '../models/InternshipCreate';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class InternshipsService {

    /**
     * Get Internships
     * Returns all internships from the database
     * @param skip
     * @param limit
     * @returns Internship Successful Response
     * @throws ApiError
     */
    public static getInternships(
skip?: number,
limit: number = 100,
): CancelablePromise<Array<Internship>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/internships/',
            query: {
                'skip': skip,
                'limit': limit,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Internship
     * Adds an Internship object to the database.
     * @param requestBody
     * @returns Internship Successful Response
     * @throws ApiError
     */
    public static createInternship(
requestBody: InternshipCreate,
): CancelablePromise<Internship> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/internships/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Search Internships
     * Searches the database for internships
     * @param q
     * @param skip
     * @param limit
     * @returns Internship Successful Response
     * @throws ApiError
     */
    public static searchInternships(
q?: string,
skip?: number,
limit: number = 100,
): CancelablePromise<Array<Internship>> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/internships/search',
            query: {
                'q': q,
                'skip': skip,
                'limit': limit,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
