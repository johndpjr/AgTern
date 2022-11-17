import {Component, Input, OnInit} from '@angular/core';
import {Internship} from "../../_generated/api";

@Component({
  selector: 'app-internship-card',
  templateUrl: './internship-card.component.html',
  styleUrls: ['./internship-card.component.scss']
})
export class InternshipCardComponent {
    @Input() internship!: Internship
}