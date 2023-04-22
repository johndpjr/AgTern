import {Component, Input, OnInit} from '@angular/core';
import {Job} from "../../_generated/api";
import {animate, style, transition, trigger} from "@angular/animations";

@Component({
  selector: 'app-job-details',
  templateUrl: './job-details.component.html',
  styleUrls: ['./job-details.component.scss'],
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
export class JobDetailsComponent {
  @Input() public job!: Job

  tags: string[] = []

  ngOnInit(): void {
    let all_tags = (
      "cloud electrical management sales big-data " +
      "ui web-dev finance robotics research " +
      "ai nlp design c++ python " +
      "database statistics seo devops security " +
      "java c# rust"
    ).split(" ").sort(() => 0.5 - Math.random())
    this.tags = all_tags.slice(0, Math.floor(Math.random() * 8) + 3)
  }
}
