import { Component, Input } from '@angular/core';
import { Job, JobStatusType } from '../../../../_generated/api';
import { animate, style, transition, trigger } from '@angular/animations';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-job-details',
  templateUrl: './job-details.component.html',
  styleUrls: ['./job-details.component.scss'],
  animations: [
    trigger('enterLeave', [
      transition(':enter', [
        style({ opacity: 0, transform: 'translateY(1em)' }),
        animate('250ms', style({ opacity: 1, transform: 'translateY(0)' }))
      ]),
      transition(':leave', [animate('100ms', style({ opacity: 0 }))]),
      transition('* => *', [
        style({ opacity: 0, transform: 'translateY(1em)' }),
        animate('250ms', style({ opacity: 1, transform: 'translateY(0)' }))
      ])
    ])
  ]
})
export class JobDetailsComponent {
  @Input() public job!: Job;

  jobStatusList: JobStatusType[] = [
    'unapplied',
    'applying',
    'applied',
    'waiting',
    'interviewing',
    'offer_pending',
    'offer_given',
    'offer_rescinded',
    'rejected',
    'withdrew',
    'unknown',
    'accepted_offer',
    'rejected_offer',
    'negotiating_offer'
  ];

  eventForm: FormGroup;
  dtPickerConfig = {
    showSpinners: true,
    stepMinute: 15,
    touchUi: false,
    enableMeridian: true,
    defaultTime: [9, 0, 0] // 09:00:00 (H, M, S)
  };

  constructor(private fb: FormBuilder) {
    this.eventForm = this.fb.group({
      title: '',
      event_category_id: '',
      dt_start: '',
      dt_end: '',
      description: ''
    });
  }

  ngOnInit(): void {}

  onEventFormSubmit() {}
}
