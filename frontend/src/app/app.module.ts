import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppComponent} from './app.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {ProfileDialogComponent} from './profile-dialog/profile-dialog.component';
import {ToolbarComponent} from './toolbar/toolbar.component';
import {SidebarComponent} from './sidebar/sidebar.component';
import {InternshipListComponent} from './internship-list/internship-list.component';
import {InternshipDetailsComponent} from './internship-details/internship-details.component';
import {InternshipCardComponent} from './internship-card/internship-card.component';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MaterialModule} from "./modules/material/material.module";
import {MAT_FORM_FIELD_DEFAULT_OPTIONS} from "@angular/material/form-field";

@NgModule({
  declarations: [
    AppComponent,
    InternshipCardComponent,
    InternshipDetailsComponent,
    InternshipListComponent,
    ProfileDialogComponent,
    SidebarComponent,
    ToolbarComponent,
  ],
  imports: [
    BrowserAnimationsModule,
    BrowserModule,
    FormsModule,
    MaterialModule,
    ReactiveFormsModule,
  ],
  providers: [
    {
      provide: MAT_FORM_FIELD_DEFAULT_OPTIONS,
      useValue: {
        appearance: "outline"
      }
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
