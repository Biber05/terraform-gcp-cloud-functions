import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {ListViewComponent} from './list-view/list-view.component';


const routes: Routes = [
  {path: 'todos', component: ListViewComponent, pathMatch: 'full'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
