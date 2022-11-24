import {Component, Input, OnInit} from '@angular/core';
import {Internship} from "../../_generated/api";
import {animate, style, transition, trigger} from "@angular/animations";

@Component({
  selector: 'app-internship-details',
  templateUrl: './internship-details.component.html',
  styleUrls: ['./internship-details.component.scss'],
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
export class InternshipDetailsComponent {
  @Input() public internship!: Internship
}
