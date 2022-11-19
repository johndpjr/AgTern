/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Season } from './Season';

export type InternshipCreate = {
    id?: number;
    job_id?: string;
    company?: string;
    title?: string;
    category?: string;
    link?: string;
    apply_link?: string;
    period?: Season;
    year?: number;
    post_date?: string;
    location?: string;
    description?: string;
};
