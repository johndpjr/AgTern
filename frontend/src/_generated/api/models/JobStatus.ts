/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { JobStatusType } from './JobStatusType';

/**
 * Models job status.
 */
export type JobStatus = {
    id?: number;
    status?: JobStatusType;
    description?: string;
};
