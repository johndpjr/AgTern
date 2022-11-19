import { Component, OnInit } from '@angular/core';

@Component({
  selector:    'app-profile-dialog',
  templateUrl: './profile-dialog.component.html',
  styleUrls:   [ './profile-dialog.component.css']
})
export class ProfileDialogComponent implements OnInit {
  major = 'cpsc';
  graduation_month = '1';
  graduation_year = '2022';

  constructor() { }

  ngOnInit(): void {
  }

}
