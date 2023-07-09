/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Job } from '../models/Job';
import type { JobCreate } from '../models/JobCreate';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class JobsService {

    /**
     * Get Jobs
     * Returns all jobs from the database.
     * @param skip
     * @param limit
     * @returns Job Successful Response
     * @throws ApiError
     */
    public static getJobs(
        skip?: number,
        limit: number = 100,
    ): CancelablePromise<Array<Job>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/jobs/',
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
     * Create Job
     * Adds a Job object to the database.
     * @param requestBody
     * @returns Job Successful Response
     * @throws ApiError
     */
    public static createJob(
        requestBody: JobCreate,
    ): CancelablePromise<Job> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/jobs/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Search Jobs
     * Searches the database for jobs.
     * @param q
     * @param skip
     * @param limit
     * @returns Job Successful Response
     * @throws ApiError
     */
    public static searchJobs(
        q?: string,
        skip?: number,
        limit: number = 100,
    ): CancelablePromise<Array<Job>> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/jobs/search',
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
