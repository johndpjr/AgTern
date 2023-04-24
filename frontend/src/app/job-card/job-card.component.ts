import {Component, Input, OnInit} from '@angular/core';
import {Job} from "../../_generated/api";

@Component({
  selector: 'app-job-card',
  templateUrl: './job-card.component.html',
  styleUrls: ['./job-card.component.scss']
})
export class JobCardComponent implements OnInit {
  @Input() job!: Job

  ngOnInit(): void {
  }
}
