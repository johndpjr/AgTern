import {NgModule} from '@angular/core';
import {MatButtonModule} from "@angular/material/button"
import {MatCardModule} from "@angular/material/card"
import {MatChipsModule} from "@angular/material/chips"
import {MatDialogModule} from "@angular/material/dialog"
import {MatDividerModule} from "@angular/material/divider"
import {MAT_FORM_FIELD_DEFAULT_OPTIONS} from "@angular/material/form-field"
import {MatIconModule} from "@angular/material/icon"
import {MatInputModule} from "@angular/material/input"
import {MatSelectModule} from "@angular/material/select"
import {MatSidenavModule} from "@angular/material/sidenav"
import {MatToolbarModule} from "@angular/material/toolbar"
import {BrowserModule} from '@angular/platform-browser';

import {AppComponent} from './app.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {ProfileDialogComponent} from './profile-dialog/profile-dialog.component';
import {ToolbarComponent} from './toolbar/toolbar.component';
import {SidebarComponent} from './sidebar/sidebar.component';
import {InternshipListComponent} from './internship-list/internship-list.component';
import {InternshipDetailsComponent} from './internship-details/internship-details.component';
import {InternshipCardComponent} from './internship-card/internship-card.component';

@NgModule({
  declarations: [
    AppComponent,
    ProfileDialogComponent,
    ToolbarComponent,
    SidebarComponent,
    InternshipListComponent,
    InternshipDetailsComponent,
    InternshipCardComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatSidenavModule,
    MatCardModule,
    MatChipsModule,
    MatInputModule,
    MatSelectModule,
    MatDividerModule,
    MatDialogModule
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
