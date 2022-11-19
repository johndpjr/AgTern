import {Component, Input, OnInit} from '@angular/core';
import {Internship} from "../../_generated/api";

@Component({
  selector: 'app-internship-details',
  templateUrl: './internship-details.component.html',
  styleUrls: ['./internship-details.component.scss']
})
export class InternshipDetailsComponent {
  @Input() public internship!: Internship
}
