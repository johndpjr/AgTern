import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MainComponent } from './main.component';
import { LoginComponent } from '../../pages/login/login.component';
import { SignUpComponent } from '../../pages/sign-up/sign-up.component';
import { NotFoundComponent } from '../../pages/not-found/not-found.component';

const routes: Routes = [
  {
    path: '',
    component: MainComponent,
    children: [
      {
        path: 'jobs',
        loadChildren: () =>
          import('../../feature/jobs/jobs.module').then((m) => m.JobsModule),
        title: 'AgTern | Jobs'
      },
      { path: 'login', component: LoginComponent, title: 'AgTern | Log In' },
      {
        path: 'sign-up',
        component: SignUpComponent,
        title: 'AgTern | Sign Up'
      }
    ]
  },
  {
    path: '**',
    component: NotFoundComponent,
    title: 'AgTern | 404 Not Found Error Helpa'
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MainRoutingModule {}
