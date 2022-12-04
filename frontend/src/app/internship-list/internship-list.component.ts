import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {Internship} from "../../_generated/api";
import {animate, style, transition, trigger} from "@angular/animations";

export type InternshipClickedEvent = {
  index: number
  internship: Internship
}

@Component({
  selector: 'app-internship-list',
  templateUrl: './internship-list.component.html',
  styleUrls: ['./internship-list.component.scss'],
  animations: [
    trigger('enterLeave', [
      transition(':enter', [
        style({ opacity: 0, transform: 'translateY(1em)' }),
        animate('250ms', style({ opacity: 1, transform: 'translateY(0)' })),
      ]),
      transition(':leave', [
        animate('100ms', style({ opacity: 0 }))
      ]),
      transition('* => *', [
        style({ opacity: 0, transform: 'translateY(1em)' }),
        animate('250ms', style({ opacity: 1, transform: 'translateY(0)' })),
      ])
    ])
  ]
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
