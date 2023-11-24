import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { JobsRoutingModule } from './jobs-routing.module';
import { JobsComponent } from './jobs.component';
import { SearchModule } from './search/search.module';
import { MaterialModule } from '../../shared/modules/material/material.module';
import { JobCardComponent } from './job-card/job-card.component';
import { JobDetailsComponent } from './job-details/job-details.component';
import { JobListComponent } from './job-list/job-list.component';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { ReactiveFormsModule } from '@angular/forms';
import { MatNativeDateModule } from '@angular/material/core';

@NgModule({
  declarations: [
    JobsComponent,
    JobListComponent,
    JobCardComponent,
    JobDetailsComponent
  ],
  exports: [JobCardComponent],
  imports: [
    CommonModule,
    JobsRoutingModule,
    MaterialModule,
    SearchModule,
    MatDatepickerModule,
    MatNativeDateModule,
    ReactiveFormsModule
  ]
})
export class JobsModule {}
