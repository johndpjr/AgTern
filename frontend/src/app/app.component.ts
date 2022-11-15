import { Component }               from '@angular/core';
import { MatDialog }              from "@angular/material/dialog"
import { ProfileDialogComponent } from "./profile-dialog/profile-dialog.component"

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: [ './app.component.scss' ]
})
export class AppComponent {
  title = 'agtern-client';
  sort = 'relevance';
  major = 'cpsc';
  season = 'summer';
  year = '2022';
  
  constructor(public dialog: MatDialog) {}
  
  openSettings() {
    this.dialog.open(ProfileDialogComponent)
  }
}
