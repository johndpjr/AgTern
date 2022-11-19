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
     * Get All Internships
     * Returns all internships from the database
     * @returns Internship Successful Response
     * @throws ApiError
     */
    public static getAllInternships(): CancelablePromise<Array<Internship>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/internships/',
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

}
