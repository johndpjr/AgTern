import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { SignUpComponent } from './pages/sign-up/sign-up.component';
import { JobsComponent } from './pages/jobs/jobs.component';
import { NotFoundComponent } from './pages/not-found/not-found.component';

const routes: Routes = [
  {
    path: '',
    loadChildren: () =>
      import('./core/main/main.module').then((m) => m.MainModule),
    title: 'AgTern',
    children: [
      { path: 'jobs', component: JobsComponent, title: 'AgTern | Jobs' },
      { path: 'login', component: LoginComponent, title: 'AgTern | Log In' },
      {
        path: 'sign-up',
        component: SignUpComponent,
        title: 'AgTern | Sign Up'
      }
    ]
  },
  { path: '**', component: NotFoundComponent, title: 'AgTern | 404 Not Found' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
