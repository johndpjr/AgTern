import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { JobsComponent } from './jobs.component';

const routes: Routes = [
  { path: '', component: JobsComponent },
  {
    path: 'jobs',
    loadChildren: () =>
      import('./search/search.module').then((m) => m.SearchModule)
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class JobsRoutingModule {}
