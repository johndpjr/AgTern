import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { NotFoundComponent } from './pages/not-found/not-found.component';

const routes: Routes = [
  {
    path: '',
    loadChildren: () =>
      import('./core/main/main.module').then((m) => m.MainModule),
    title: 'AgTern'
  },
  {
    path: '**',
    component: NotFoundComponent,
    title: 'AgTern | 404 Not Found Error Helpa'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: true })],
  exports: [RouterModule]
})
export class AppRoutingModule {}
