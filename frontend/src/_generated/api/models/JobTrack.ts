/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { JobStatusType } from './JobStatusType';

/**
 * Models job track items.
 */
export type JobTrack = {
    status?: JobStatusType;
    timestamp?: string;
    id?: number;
    user_job_track_id?: number;
};
