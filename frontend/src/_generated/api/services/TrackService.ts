/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { JobTrack } from '../models/JobTrack';
import type { JobTrackCreate } from '../models/JobTrackCreate';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class TrackService {

    /**
     * Get Track Points
     * Returns all jobs.
     * @param jobId
     * @returns JobTrack Successful Response
     * @throws ApiError
     */
    public static getTrackPoints(
        jobId: number,
    ): CancelablePromise<Array<JobTrack>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/track/',
            query: {
                'job_id': jobId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Track Point
     * Adds a JobTrack.
     * @param requestBody
     * @returns JobTrack Successful Response
     * @throws ApiError
     */
    public static createTrackPoint(
        requestBody: JobTrackCreate,
    ): CancelablePromise<JobTrack> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/track/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Track Statuses
     * Returns all job track statuses.
     * @returns JobTrack Successful Response
     * @throws ApiError
     */
    public static getTrackStatuses(): CancelablePromise<Array<JobTrack>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/track/statuses',
        });
    }

}
