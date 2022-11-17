import {Component, Input, OnInit} from '@angular/core';
import {Internship} from "../../_generated/api";

@Component({
  selector: 'app-internship-list',
  templateUrl: './internship-list.component.html',
  styleUrls: ['./internship-list.component.scss']
})
export class InternshipListComponent {
    @Input() internships: Internship[] = []
}
