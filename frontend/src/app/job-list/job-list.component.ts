import {Component, EventEmitter, Input, Output} from '@angular/core';
import {Job} from "../../_generated/api";
import {animate, style, transition, trigger} from "@angular/animations";

export type JobClickedEvent = {
  index: number
  job: Job
}

@Component({
  selector: 'app-job-list',
  templateUrl: './job-list.component.html',
  styleUrls: ['./job-list.component.scss'],
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
export class JobListComponent {
  @Input() jobs: Job[] = []
  @Output() jobClicked: EventEmitter<JobClickedEvent> = new EventEmitter()

  onJobClicked(index: number) {
    this.jobClicked.emit({
      index: index,
      job: this.jobs[index]
    })
  }
}
