import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Internship} from "../../_generated/api";

export type InternshipClickedEvent = {
  index: number
  internship: Internship
}

@Component({
  selector: 'app-internship-list',
  templateUrl: './internship-list.component.html',
  styleUrls: ['./internship-list.component.scss']
})
export class InternshipListComponent {
  @Input() internships: Internship[] = []
  @Output() internshipClicked: EventEmitter<InternshipClickedEvent> = new EventEmitter()

  onInternshipClicked(index: number) {
    this.internshipClicked.emit({
      index: index,
      internship: this.internships[index]
    })
  }
}
