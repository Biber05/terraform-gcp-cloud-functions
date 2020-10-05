import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {ListViewComponent} from './list-view/list-view.component';
import {CreateTodoComponent} from './create-todo/create-todo.component';
import {ListViewItemComponent} from './list-view/list-view-item/list-view-item/list-view-item.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatListModule} from '@angular/material/list';

@NgModule({
  declarations: [
    AppComponent,
    ListViewComponent,
    CreateTodoComponent,
    ListViewItemComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatListModule,
    BrowserAnimationsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
