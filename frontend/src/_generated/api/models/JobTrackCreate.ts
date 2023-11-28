/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { JobStatusType } from './JobStatusType';

export type JobTrackCreate = {
    status?: JobStatusType;
    timestamp?: string;
    job_id?: number;
};
