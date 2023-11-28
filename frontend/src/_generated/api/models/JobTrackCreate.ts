/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { JobStatusType } from './JobStatusType';

export type JobTrackCreate = {
    id?: number;
    job_status?: JobStatusType;
    user_job_track_id?: number;
    timestamp?: string;
};
