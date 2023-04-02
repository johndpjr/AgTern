/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Season } from './Season';

/**
 * Models job details.
 */
export type Job = {
    id?: number;
    company_job_id?: string;
    company?: string;
    title?: string;
    type?: string;
    category?: string;
    posting_link?: string;
    apply_link?: string;
    period?: Season;
    year?: number;
    post_date?: string;
    location?: string;
    description?: string;
    tags?: string;
};
