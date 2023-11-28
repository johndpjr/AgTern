/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { JobStatusType } from './JobStatusType';

/**
 * Models job track items.
 */
export type JobTrack = {
    id?: number;
    job_status?: JobStatusType;
    user_job_track_id?: number;
    timestamp?: string;
};
