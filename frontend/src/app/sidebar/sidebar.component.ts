import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {FormControl} from "@angular/forms";
import {debounceTime} from "rxjs";

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {
  search = new FormControl('');
  sort = new FormControl('alpha');
  major = new FormControl('cpen');
  season = new FormControl('summer');
  year = new FormControl('2022');

  @Output() searchChanged = new EventEmitter<string>();

  ngOnInit(): void {
    this.search.valueChanges
      .pipe(debounceTime(500))
      .subscribe(next => this.searchChanged.emit(next ?? ""))
  }
}
